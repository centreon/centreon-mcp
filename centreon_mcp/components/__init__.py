from centreon_mcp.components.host import host
from centreon_mcp.components.hostgroup import hostgroup
from centreon_mcp.components.service import service
from centreon_mcp.components.servicegroup import servicegroup

components = {
    "host": host,
    "service": service,
    "hostgroup": hostgroup,
    "servicegroup": servicegroup,
}
