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
    # Initialize Centreon client
    request.client = AsyncClient(
        verify=settings.verify,
        timeout=settings.client_timeout,
        base_url=f"{settings.base_url}/api/latest",
    )
    logger.info(
        f"Centreon API Client initialized (\n"
        f"\ttimeout={settings.client_timeout},\n"
        f"\ttls_secure={settings.tls_secure},\n"
        f"\tca_bundle={settings.ca_bundle},\n"
        f"\tbase_url={request.client.base_url}\n"
        ")."
    )

    # Test Centreon API connectivity and get web version
    version = await Platform.get_web_version()
    logger.info(f"Connected to Centreon API version {version.version}")

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
