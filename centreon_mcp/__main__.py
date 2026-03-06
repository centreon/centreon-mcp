import logging

from centreon_mcp import CREDENTIALS
from centreon_mcp.server import mcp
from centreon_mcp.utils import logger


def main():

    # Set log level from environment variable
    level = CREDENTIALS["CENTREON_MCP_LOG_LEVEL"]
    try:
        logger.setLevel(level)
    except ValueError:
        logger.setLevel(logging.INFO)
        logger.warning(f"Invalid log level '{level}' set. Defaulting to INFO.")

    # Start Centreon MCP
    mcp.run(transport="http", port=int(CREDENTIALS["CENTREON_MCP_PORT"]))


if __name__ == "__main__":
    main()
