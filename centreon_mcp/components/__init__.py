from centreon_mcp.components.configuration import configuration
from centreon_mcp.components.metric import metric
from centreon_mcp.components.monitoring import monitoring
from centreon_mcp.components.monitoring_server import monitoring_server
from centreon_mcp.components.timeline import timeline

components = [monitoring, monitoring_server, metric, timeline, configuration]
