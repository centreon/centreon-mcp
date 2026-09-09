from contextlib import asynccontextmanager

from fastmcp import FastMCP
from httpx import AsyncClient

from centreon_mcp import CREDENTIALS
from centreon_mcp.components import components
from centreon_mcp.types.platform import Platform
from centreon_mcp.utils import logger, request


@asynccontextmanager
async def lifespan(app: FastMCP):
    """
    Lifespan context manager for FastMCP application.
    """
    # Check if Centreon API token is provided
    for credential in ["CENTREON_BASE_URL"]:
        if not CREDENTIALS[credential]:
            msg = f"{credential} is missing. Don't starting MCP server."
            raise RuntimeError(msg)

    # Initialize Centreon client
    request.client = AsyncClient()

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
