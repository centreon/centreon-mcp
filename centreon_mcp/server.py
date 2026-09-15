from contextlib import asynccontextmanager

from fastmcp import FastMCP
from httpx import AsyncClient, HTTPError
from mcp.types import Icon
from starlette.requests import Request
from starlette.responses import JSONResponse

from centreon_mcp import settings
from centreon_mcp.auth import get_plugin
from centreon_mcp.components import components
from centreon_mcp.types.platform import Platform
from centreon_mcp.utils import logger, request
from centreon_mcp.utils.request import CentreonAPIError


async def check_tenants() -> None:
    """
    Prove connectivity to the Centreon the server is configured with.

    A single tenant that cannot be reached prevents the server from starting. When several
    tenants are served, one unreachable customer must not take the shared server down, so only a
    complete failure aborts the startup.
    """
    tenants = get_plugin().tenants()
    if tenants is None:
        logger.info(
            f"The '{settings.auth_plugin}' plugin resolves its Centreon per request, "
            "so none is checked at startup"
        )
        return

    if not tenants:
        logger.warning(
            f"The '{settings.auth_plugin}' plugin expects tenants and has none, so no Centreon is "
            "checked at startup and every request will fail. Check its configuration."
        )
        return

    unreachable = []
    for tenant in tenants:
        try:
            version = await Platform.get_web_version(tenant=tenant)
            logger.info(f"Connected to Centreon API version {version.version} for {tenant.name}")
        except (CentreonAPIError, HTTPError) as error:
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
    # Initialize Centreon client
    request.client = AsyncClient(timeout=settings.client_timeout)

    # Test Centreon API connectivity and get web version
    await check_tenants()

    # Import components, including those the authentication plugin adds. Mounted once for the
    # life of the app: an app started again in the same process would otherwise carry every tool
    # twice, and the duplicates shadow each other in listings
    global mounted
    if not mounted:
        for server in [*components, *get_plugin().components()]:
            app.mount(server)
        mounted = True

    yield

    # Close Centreon Client
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
