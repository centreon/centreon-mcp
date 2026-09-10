from contextlib import asynccontextmanager

from fastmcp import FastMCP
from httpx import AsyncClient

from centreon_mcp import settings
from centreon_mcp.components import components
from centreon_mcp.types.platform import Platform
from centreon_mcp.utils import logger, request


@asynccontextmanager
async def lifespan(app: FastMCP):
    """
    Lifespan context manager for FastMCP application.
    """
    # Initialize Centreon client
    request.client = AsyncClient(timeout=settings.client_timeout)

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
