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

    # Test Centreon API connectivity and get web version
    version = await Platform.get_web_version()
    logger.info(f"Connected to Centreon API version {version.version}")

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

    It answers without authentication, since a probe holds no token, and says nothing about
    Centreon: the server is up whether or not the platform it calls answers.
    """
    return JSONResponse({"status": "ok"})


def main():

    # Set log level from environment variable
    logger.setLevel(settings.mcp_log_level)

    # Start Centreon MCP
    mcp.run(transport="http", host=settings.mcp_host, port=settings.mcp_port)


if __name__ == "__main__":
    main()
