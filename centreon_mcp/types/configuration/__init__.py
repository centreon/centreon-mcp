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
from centreon_mcp.types.configuration.service import (
    Service,
    ServiceFilter,
    ServiceFullParams,
    ServiceOrder,
    ServicePartialParams,
)
from centreon_mcp.types.configuration.service_category import (
    ServiceCategory,
    ServiceCategoryFilter,
    ServiceCategoryFullParams,
    ServiceCategoryOrder,
)
from centreon_mcp.types.configuration.service_group import (
    ServiceGroup,
    ServiceGroupFilter,
    ServiceGroupFullParams,
    ServiceGroupOrder,
)
from centreon_mcp.types.configuration.service_severity import (
    ServiceSeverity,
    ServiceSeverityFilter,
    ServiceSeverityFullParams,
    ServiceSeverityOrder,
    ServiceSeverityPartialParams,
)
from centreon_mcp.types.configuration.service_template import (
    ServiceTemplate,
    ServiceTemplateFilter,
    ServiceTemplateFullParams,
    ServiceTemplateOrder,
    ServiceTemplatePartialParams,
)

ConfigurationFilter = Annotated[
    CommandFilter
    | HostCategoryFilter
    | HostGroupFilter
    | HostSeverityFilter
    | HostTemplateFilter
    | HostFilter
    | ServiceFilter
    | ServiceCategoryFilter
    | ServiceGroupFilter
    | ServiceTemplateFilter
    | ServiceSeverityFilter
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
    | ServiceOrder
    | ServiceCategoryOrder
    | ServiceGroupOrder
    | ServiceTemplateOrder
    | ServiceSeverityOrder
    | MonitoringServerOrder,
    Field(discriminator="model_type"),
]

ConfigurationFullParams = Annotated[
    HostCategoryFullParams
    | HostGroupFullParams
    | HostSeverityFullParams
    | HostTemplateFullParams
    | HostFullParams
    | ServiceFullParams
    | ServiceCategoryFullParams
    | ServiceGroupFullParams
    | ServiceTemplateFullParams
    | ServiceSeverityFullParams
    | CommandParams,
    Field(discriminator="model_type"),
]

ConfigurationPartialParams = Annotated[
    HostCategoryPartialParams
    | HostGroupPartialParams
    | HostSeverityPartialParams
    | HostTemplatePartialParams
    | HostPartialParams
    | ServicePartialParams
    | ServiceTemplatePartialParams
    | ServiceSeverityPartialParams,
    Field(discriminator="model_type"),
]

Configuration = (
    Command
    | HostCategory
    | HostGroup
    | HostSeverity
    | HostTemplate
    | Host
    | MonitoringServer
    | Service
    | ServiceCategory
    | ServiceGroup
    | ServiceTemplate
    | ServiceSeverity
)
