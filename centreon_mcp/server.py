from contextlib import asynccontextmanager

from fastmcp import FastMCP

from centreon_mcp.utils.logger import logger
from centreon_mcp.utils.request import CentreonAPIError, request


@asynccontextmanager
async def lifespan(app: FastMCP):
    """
    Lifespan context manager for FastMCP application.
    """
    # Test Centreon API connectivity
    try:
        result = await request("GET", "platform/versions")
    except CentreonAPIError:
        logger.error("Failed to connect to Centreon API")
        raise
    else:
        version = result["web"]["version"]
        logger.info(f"Connected to Centreon API version {version}")

    yield


mcp = FastMCP(name="Centreon MCP Server", lifespan=lifespan)
