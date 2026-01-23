# Centreon MCP Server

This project offers an MCP server for Centreon. Built in Python with the [FastMcp](https://gofastmcp.com/getting-started/welcome) library, it enables users to perform operations on a Centreon instance using natural language commands.

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

3. Set environment variables

```shell
export CENTREON_HOST="your_centreon_host"   # default: localhost
export CENTREON_PORT="your_centreon_port"   # default: 4000 
export CENTREON_API_TOKEN="your_centreon_api_token"    
```

4. Start the MCP server

```shell
uv run fastmcp run centreon_mcp/server.py --transport http --port 8000
```



