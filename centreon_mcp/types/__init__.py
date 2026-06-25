from centreon_mcp.types.configuration.command import Command
from centreon_mcp.types.configuration.host import HostConfiguration
from centreon_mcp.types.configuration.host_category import HostCategoryConfiguration
from centreon_mcp.types.configuration.host_group import HostGroupConfiguration
from centreon_mcp.types.configuration.host_severity import HostSeverity
from centreon_mcp.types.configuration.host_template import HostTemplate
from centreon_mcp.types.configuration.monitoring_server import MonitoringServerConfiguration
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, PatchMixin, UpdateMixin

MODELS_MIXIN_LIST: dict[str, type[ListMixin]] = {
    model.model_type: model
    for model in [
        HostConfiguration,
        HostGroupConfiguration,
        HostCategoryConfiguration,
        HostSeverity,
        HostTemplate,
        Command,
        MonitoringServerConfiguration,
    ]
}

MODELS_MIXIN_CREATE: dict[str, type[CreateMixin]] = {
    model.model_type: model
    for model in [
        HostConfiguration,
        HostGroupConfiguration,
        HostCategoryConfiguration,
        HostSeverity,
        HostTemplate,
        Command,
    ]
}

MODELS_MIXIN_UPDATE: dict[str, type[UpdateMixin]] = {
    model.model_type: model
    for model in [
        HostGroupConfiguration,
        HostCategoryConfiguration,
        HostSeverity,
    ]
}

MODELS_MIXIN_PATCH: dict[str, type[PatchMixin]] = {
    model.model_type: model for model in [HostConfiguration, HostTemplate]
}


MODELS_MIXIN_DELETE: dict[str, type[DeleteMixin]] = {
    model.model_type: model
    for model in [
        HostConfiguration,
        HostGroupConfiguration,
        HostCategoryConfiguration,
        HostSeverity,
        HostTemplate,
    ]
}
