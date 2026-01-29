from centreon_mcp import CREDENTIALS
from centreon_mcp.server import mcp


def main():
    mcp.run(transport="http", port=int(CREDENTIALS["CENTREON_MCP_PORT"]))


if __name__ == "__main__":
    main()
