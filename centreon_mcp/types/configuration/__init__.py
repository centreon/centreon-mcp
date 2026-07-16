from typing import Annotated

from pydantic import Field

from centreon_mcp.types.configuration.command import (
    Command,
    CommandFilter,
    CommandOrder,
    CommandParams,
)
from centreon_mcp.types.configuration.host import (
    Host,
    HostFilter,
    HostFullParams,
    HostOrder,
    HostPartialParams,
)
from centreon_mcp.types.configuration.host_category import (
    HostCategory,
    HostCategoryFilter,
    HostCategoryFullParams,
    HostCategoryOrder,
    HostCategoryPartialParams,
)
from centreon_mcp.types.configuration.host_group import (
    HostGroup,
    HostGroupFilter,
    HostGroupFullParams,
    HostGroupOrder,
    HostGroupPartialParams,
)
from centreon_mcp.types.configuration.host_severity import (
    HostSeverity,
    HostSeverityFilter,
    HostSeverityFullParams,
    HostSeverityOrder,
    HostSeverityPartialParams,
)
from centreon_mcp.types.configuration.host_template import (
    HostTemplate,
    HostTemplateFilter,
    HostTemplateFullParams,
    HostTemplateOrder,
    HostTemplatePartialParams,
)
from centreon_mcp.types.configuration.monitoring_server import (
    MonitoringServer,
    MonitoringServerFilter,
    MonitoringServerOrder,
)

ConfigurationFilter = Annotated[
    CommandFilter
    | HostCategoryFilter
    | HostGroupFilter
    | HostSeverityFilter
    | HostTemplateFilter
    | HostFilter
    | MonitoringServerFilter,
    Field(discriminator="model_type"),
]

ConfigurationOrder = Annotated[
    CommandOrder
    | HostCategoryOrder
    | HostGroupOrder
    | HostSeverityOrder
    | HostTemplateOrder
    | HostOrder
    | MonitoringServerOrder,
    Field(discriminator="model_type"),
]

ConfigurationFullParams = Annotated[
    HostCategoryFullParams
    | HostGroupFullParams
    | HostSeverityFullParams
    | HostTemplateFullParams
    | HostFullParams
    | CommandParams,
    Field(discriminator="model_type"),
]

ConfigurationPartialParams = Annotated[
    HostCategoryPartialParams
    | HostGroupPartialParams
    | HostSeverityPartialParams
    | HostTemplatePartialParams
    | HostPartialParams,
    Field(discriminator="model_type"),
]

Configuration = (
    Command | HostCategory | HostGroup | HostSeverity | HostTemplate | Host | MonitoringServer
)
