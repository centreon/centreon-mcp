# Centreon MCP Server

This project offers an MCP server for Centreon. Built in Python with the [FastMCP](https://gofastmcp.com/getting-started/welcome) library, it enables users to perform operations on a Centreon instance using natural language commands.

## Quick Start

1. Clone the repository

```shell
git clone https://github.com/centreon/centreon-mcp.git
cd centreon-mcp
```

2. Install dependencies and synchronize

```shell
uv sync
```

3. Ensure all required environment variables are set. Default values are used for optional variables.

| Name                     | Default | Description                                           |
| ------------------------ | ------- | ----------------------------------------------------- |
| `CENTREON_BASE_URL`      |         | Base URL of the Centreon instance.                    |
| `CENTREON_API_TOKEN`     |         | Token used to access the Centreon API through MCP.    |
| `CENTREON_MCP_PORT`      | `8000`  | Port used to start the Centreon MCP service.          |
| `CENTREON_MCP_LOG_LEVEL` | `INFO`  | Minimal severity level for Centreon MCP service logs. |

4. Start the MCP server

```shell
uv run mcp
```



