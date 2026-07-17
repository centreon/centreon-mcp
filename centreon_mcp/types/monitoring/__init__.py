from typing import Annotated

from pydantic import Field

from centreon_mcp.types.monitoring.host_group import HostGroup, HostGroupFilter, HostGroupOrder
from centreon_mcp.types.monitoring.monitoring_server import (
    MonitoringServer,
    MonitoringServerFilter,
    MonitoringServerOrder,
)
from centreon_mcp.types.monitoring.servicegroup import (
    ServiceGroup,
    ServiceGroupFilter,
    ServiceGroupOrder,
)

MonitoringFilter = Annotated[
    HostGroupFilter | ServiceGroupFilter | MonitoringServerFilter,
    Field(discriminator="model_type"),
]


MonitoringOrder = Annotated[
    HostGroupOrder | ServiceGroupOrder | MonitoringServerOrder,
    Field(discriminator="model_type"),
]


Monitoring = HostGroup | ServiceGroup | MonitoringServer
