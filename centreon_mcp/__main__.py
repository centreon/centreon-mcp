from contextlib import asynccontextmanager

from fastmcp import FastMCP
from httpx import AsyncClient
from mcp.types import Icon
from starlette.requests import Request
from starlette.responses import JSONResponse

from centreon_mcp import logger, settings
from centreon_mcp.auth import get_plugin
from centreon_mcp.components import components
from centreon_mcp.types.platform import Platform
from centreon_mcp.utils import request


async def check_tenants() -> None:
    """
    Prove connectivity to the Centreon instances the server is configured with.

    With a single tenant configured, failing to reach it stops the server. When several are
    served, one unreachable customer must not take the shared server down, so only a complete
    failure aborts the startup.
    """
    tenants = get_plugin().tenants()
    if tenants is None:
        logger.info(
            f"The '{settings.auth_plugin}' plugin resolves its Centreon per request, "
            "so none is checked at startup"
        )
        return

    if not tenants:
        logger.error(
            f"The '{settings.auth_plugin}' plugin expects tenants and has none, so no Centreon is "
            "checked at startup and every request will fail. Check its configuration."
        )
        return

    unreachable = []
    for tenant in tenants:
        try:
            version = await Platform.get_web_version(tenant=tenant)
            logger.info(f"Connected to Centreon API version {version.version} for {tenant.name}")
        # Deliberately broad: this is a probe, every outcome is reported by tenant name and
        # type below, and a tenant answering something other than Centreon must degrade like an
        # unreachable one rather than abort the startup of every other tenant
        except Exception as error:
            if len(tenants) == 1:
                raise
            unreachable.append(tenant.name)
            logger.warning(
                f"Centreon API is unreachable for {tenant.name}: {type(error).__name__}: {error}"
            )

    if not unreachable:
        return

    names = ", ".join(unreachable)
    if len(unreachable) == len(tenants):
        raise RuntimeError(f"Centreon API is unreachable for every tenant: {names}")

    # Nothing checks these again, so this line is the only record that the server started
    # degraded, and their users will be told the platform is down
    logger.error(f"Starting with {len(unreachable)} of {len(tenants)} tenants unreachable: {names}")


mounted = False


@asynccontextmanager
async def lifespan(app: FastMCP):
    """
    Lifespan context manager for FastMCP application.
    """
    # No base URL on the client: the Centreon to call is resolved per request, and only the TLS
    # settings are the same for all of them
    request.client = AsyncClient(verify=settings.verify, timeout=settings.client_timeout)
    logger.info(
        f"Centreon API Client initialized (\n"
        f"\ttimeout={settings.client_timeout},\n"
        f"\ttls_secure={settings.tls_secure},\n"
        f"\tca_bundle={settings.ca_bundle}\n"
        ")."
    )

    plugin = get_plugin()
    # The active plugin decides who may do what, so name it: a deployment meaning to authenticate
    # its users but whose setting never reached the process would otherwise look healthy
    logger.info(
        f"Authenticating with the '{settings.auth_plugin}' plugin"
        if plugin.auth_provider() is not None
        else f"Running unauthenticated ('{settings.auth_plugin}' plugin), "
        "every tool is granted and the Centreon token carries the rights"
    )

    await check_tenants()

    # Import components, including those the authentication plugin adds. Mounted once for the
    # life of the app: an app started again in the same process would otherwise carry every tool
    # twice, and the duplicates shadow each other in listings
    global mounted
    if not mounted:
        for server in [*components, *plugin.components()]:
            app.mount(server)
        mounted = True

    yield

    await request.client.aclose()


def icons() -> list[Icon] | None:
    return [Icon(src=settings.mcp_icon_url)] if settings.mcp_icon_url else None


mcp = FastMCP(
    name="Centreon MCP Server",
    lifespan=lifespan,
    auth=get_plugin().auth_provider(),
    icons=icons(),
    website_url=settings.mcp_website_url,
)


@mcp.custom_route("/health", methods=["GET"])
async def health(http_request: Request) -> JSONResponse:
    """
    Report that the process is up, for the probes of an orchestrator.

    It deliberately says nothing about Centreon: a platform being unreachable is not a reason to
    restart the server or to take it out of the load balancer, since the other tenants it serves
    are unaffected.
    """
    return JSONResponse({"status": "ok"})


def main():

    # Set log level from environment variable
    logger.setLevel(settings.mcp_log_level)

    # Start Centreon MCP
    mcp.run(transport="http", host=settings.mcp_host, port=settings.mcp_port)


if __name__ == "__main__":
    main()
