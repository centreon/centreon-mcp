from centreon_mcp import settings
from centreon_mcp.server import mcp
from centreon_mcp.utils import logger


def main():

    # Set log level from environment variable
    logger.setLevel(settings.mcp_log_level)

    # Start Centreon MCP
    mcp.run(transport="http", host=settings.mcp_host, port=settings.mcp_port)


if __name__ == "__main__":
    main()
