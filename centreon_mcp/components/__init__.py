from centreon_mcp.components.configuration import configuration
from centreon_mcp.components.host import host
from centreon_mcp.components.metric import metric
from centreon_mcp.components.monitoring import monitoring
from centreon_mcp.components.monitoring_server import monitoring_server
from centreon_mcp.components.service import service
from centreon_mcp.components.timeline import timeline

components = [host, monitoring, monitoring_server, service, metric, timeline, configuration]
