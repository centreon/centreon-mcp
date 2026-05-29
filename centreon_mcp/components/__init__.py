from centreon_mcp.components.acknowledgement import acknowledgement
from centreon_mcp.components.check import check
from centreon_mcp.components.command import command
from centreon_mcp.components.comment import comment
from centreon_mcp.components.downtime import downtime
from centreon_mcp.components.host import host
from centreon_mcp.components.host_category import host_category
from centreon_mcp.components.host_group import host_group
from centreon_mcp.components.host_severity import host_severity
from centreon_mcp.components.host_template import host_template
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
    command,
    check,
    timeline,
    host_severity,
    host_category,
    host_template,
]
