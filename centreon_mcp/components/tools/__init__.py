from fastmcp import FastMCP

from centreon_mcp.components.tools.configuration import configuration
from centreon_mcp.components.tools.metric import metric
from centreon_mcp.components.tools.monitoring import monitoring
from centreon_mcp.components.tools.timeline import timeline

tools = FastMCP()

tools.mount(configuration)
tools.mount(monitoring)
tools.mount(timeline)
tools.mount(metric)
