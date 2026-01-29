import os

CREDENTIALS = {
    name: (os.environ.get(name) or default)
    for name, default in [
        ("CENTREON_BASE_URL", ""),
        ("CENTREON_API_TOKEN", ""),
        ("CENTREON_MCP_LOG_LEVEL", "INFO"),
        ("CENTREON_MCP_PORT", "8000"),
    ]
}
