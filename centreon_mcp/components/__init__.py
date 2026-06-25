from centreon_mcp.components.acknowledgement import acknowledgement
from centreon_mcp.components.check import check
from centreon_mcp.components.comment import comment
from centreon_mcp.components.configuration import configuration
from centreon_mcp.components.downtime import downtime
from centreon_mcp.components.host import host
from centreon_mcp.components.host_group import host_group
from centreon_mcp.components.monitoring_server import monitoring_server
from centreon_mcp.components.resource import resource
from centreon_mcp.components.service import service
from centreon_mcp.components.servicegroup import servicegroup
from centreon_mcp.components.timeline import timeline

components = [
    resource,
    host,
    host_group,
    servicegroup,
    monitoring_server,
    downtime,
    acknowledgement,
    comment,
    service,
    check,
    timeline,
    configuration,
]
