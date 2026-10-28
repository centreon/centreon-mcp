from fastmcp import FastMCP

from centreon_mcp.components.prompts.diagnosis import diagnosis

prompts = FastMCP()

prompts.mount(diagnosis)
