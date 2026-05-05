from centreon_mcp.components.acknowledgement import acknowledgement
from centreon_mcp.components.command import command
from centreon_mcp.components.comment import comment
from centreon_mcp.components.downtime import downtime
from centreon_mcp.components.host import host
from centreon_mcp.components.hostgroup import hostgroup
from centreon_mcp.components.metric import metric
from centreon_mcp.components.monitoring_server import monitoring_server
from centreon_mcp.components.resource import resource
from centreon_mcp.components.service import service
from centreon_mcp.components.servicegroup import servicegroup

components = [
    resource,
    host,
    hostgroup,
    servicegroup,
    monitoring_server,
    downtime,
    acknowledgement,
    comment,
    service,
    command,
    metric,
]
