import os
from contextlib import asynccontextmanager

from fastmcp import FastMCP
from httpx import AsyncClient

from centreon_mcp import logger, settings
from centreon_mcp.components import components
from centreon_mcp.types.platform import Platform
from centreon_mcp.utils import request


@asynccontextmanager
async def lifespan(app: FastMCP):
    """
    Lifespan context manager for FastMCP application.
    """
    # Assert Centreon CA bundle path exists if provided
    if settings.tls_secure and settings.ca_bundle and not os.path.isfile(settings.ca_bundle):
        logger.warning(
            f"Ignoring CENTREON_CA_BUNDLE='{settings.ca_bundle}': file does not exist.\n"
            "Falling back to default/system CA trust.\n"
        )
        settings.ca_bundle = None

    # Initialize Centreon client
    request.client = AsyncClient(verify=settings.verify, timeout=settings.client_timeout)
    logger.info(
        f"Centreon API Client initialiazed (timeout={settings.client_timeout}, tls_secure={settings.tls_secure}, ca_bundle={settings.ca_bundle}).\n"
    )

    # Test Centreon API connectivity and get web version
    version = await Platform.get_web_version()
    logger.info(f"Connected to Centreon API version {version.version}\n")

    # Import components
    for server in components:
        app.mount(server)

    yield

    # Close Centreon Client
    await request.client.aclose()


mcp = FastMCP(name="Centreon MCP Server", lifespan=lifespan)


def main():

    # Set log level from environment variable
    logger.setLevel(settings.mcp_log_level)

    # Start Centreon MCP
    mcp.run(transport="http", host=settings.mcp_host, port=settings.mcp_port)


if __name__ == "__main__":
    main()
