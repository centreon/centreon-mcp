from centreon_mcp.components.acknowledgement import acknowledgement
from centreon_mcp.components.downtime import downtime
from centreon_mcp.components.host import host
from centreon_mcp.components.hostgroup import hostgroup
from centreon_mcp.components.monitoring_server import monitoring_server
from centreon_mcp.components.service import service
from centreon_mcp.components.servicegroup import servicegroup

components = [
    host,
    service,
    hostgroup,
    servicegroup,
    monitoring_server,
    downtime,
    acknowledgement,
]
