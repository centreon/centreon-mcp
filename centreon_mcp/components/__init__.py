from centreon_mcp.components.acknowledgement import acknowledgement
from centreon_mcp.components.configuration import configuration
from centreon_mcp.components.downtime import downtime
from centreon_mcp.components.host import host
from centreon_mcp.components.metric import metric
from centreon_mcp.components.monitoring import monitoring
from centreon_mcp.components.monitoring_server import monitoring_server
from centreon_mcp.components.resource import resource
from centreon_mcp.components.service import service
from centreon_mcp.components.timeline import timeline

components = [
    resource,
    host,
    monitoring,
    monitoring_server,
    downtime,
    acknowledgement,
    service,
    metric,
    timeline,
    configuration,
]
