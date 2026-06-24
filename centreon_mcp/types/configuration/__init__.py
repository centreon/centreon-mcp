from typing import Annotated

from pydantic import Field

from centreon_mcp.types.configuration.command import (
    Command,
    CommandFilter,
    CommandOrder,
    CommandParams,
)
from centreon_mcp.types.configuration.host import (
    HostConfiguration,
    HostConfigurationFilter,
    HostConfigurationFullParams,
    HostConfigurationOrder,
    HostConfigurationPartialParams,
)
from centreon_mcp.types.configuration.host_category import (
    HostCategoryConfiguration,
    HostCategoryConfigurationFilter,
    HostCategoryConfigurationFullParams,
    HostCategoryConfigurationOrder,
    HostCategoryConfigurationPartialParams,
)
from centreon_mcp.types.configuration.host_group import (
    HostGroupConfiguration,
    HostGroupConfigurationFilter,
    HostGroupConfigurationFullParams,
    HostGroupConfigurationOrder,
    HostGroupConfigurationPartialParams,
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
    MonitoringServerConfiguration,
    MonitoringServerConfigurationFilter,
    MonitoringServerConfigurationOrder,
)

ConfigurationFilter = Annotated[
    CommandFilter
    | HostCategoryConfigurationFilter
    | HostGroupConfigurationFilter
    | HostSeverityFilter
    | HostTemplateFilter
    | HostConfigurationFilter
    | MonitoringServerConfigurationFilter,
    Field(discriminator="model_type"),
]

ConfigurationOrder = Annotated[
    CommandOrder
    | HostCategoryConfigurationOrder
    | HostGroupConfigurationOrder
    | HostSeverityOrder
    | HostTemplateOrder
    | HostConfigurationOrder
    | MonitoringServerConfigurationOrder,
    Field(discriminator="model_type"),
]

ConfigurationFullParams = Annotated[
    HostCategoryConfigurationFullParams
    | HostGroupConfigurationFullParams
    | HostSeverityFullParams
    | HostTemplateFullParams
    | HostConfigurationFullParams
    | CommandParams,
    Field(discriminator="model_type"),
]

ConfigurationPartialParams = Annotated[
    HostCategoryConfigurationPartialParams
    | HostGroupConfigurationPartialParams
    | HostSeverityPartialParams
    | HostTemplatePartialParams
    | HostConfigurationPartialParams,
    Field(discriminator="model_type"),
]

Configuration = (
    Command
    | HostCategoryConfiguration
    | HostGroupConfiguration
    | HostSeverity
    | HostTemplate
    | HostConfiguration
    | MonitoringServerConfiguration
)


CONFIGURATIONS_FULL_PARAMS = {
    "host_category": HostCategoryConfigurationFullParams,
    "host_group": HostGroupConfigurationFullParams,
    "host_severity": HostSeverityFullParams,
}
