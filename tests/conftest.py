import os

os.environ.update(
    {
        "CENTREON_BASE_URL": "http://centreon.example.com",
        "CENTREON_API_TOKEN": "env-token",
        "CENTREON_MCP_HOST": "localhost",
        "CENTREON_MCP_PORT": "8000",
    }
)
