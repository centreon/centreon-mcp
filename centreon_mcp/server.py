from contextlib import asynccontextmanager

from fastmcp import FastMCP

from centreon_mcp import CREDENTIALS
from centreon_mcp.components import components
from centreon_mcp.utils.logger import logger
from centreon_mcp.utils.request import CentreonAPIError, request


@asynccontextmanager
async def lifespan(app: FastMCP):
    """
    Lifespan context manager for FastMCP application.
    """
    # Check if Centreon API token is provided
    for credential in ["CENTREON_BASE_URL", "CENTREON_API_TOKEN"]:
        if not CREDENTIALS[credential]:
            msg = f"{credential} is missing. Don't starting MCP server."
            raise RuntimeError(msg)

    # Test Centreon API connectivity
    try:
        result = await request("GET", "platform/versions")
    except CentreonAPIError as e:
        raise e
    else:
        version = result["web"]["version"]
        logger.info(f"Connected to Centreon API version {version}")

    # Import components
    for server in components:
        await app.import_server(server)

    yield


mcp = FastMCP(name="Centreon MCP Server", lifespan=lifespan)
