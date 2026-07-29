from centreon_mcp.types.configuration.command import Command
from centreon_mcp.types.configuration.host import Host
from centreon_mcp.types.configuration.host_category import HostCategory
from centreon_mcp.types.configuration.host_group import HostGroup
from centreon_mcp.types.configuration.host_severity import HostSeverity
from centreon_mcp.types.configuration.host_template import HostTemplate
from centreon_mcp.types.configuration.monitoring_server import MonitoringServer
from centreon_mcp.types.configuration.service import Service
from centreon_mcp.types.configuration.service_group import ServiceGroup
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, UpdateMixin

_list_models: list[type[ListMixin]] = [
    Host,
    HostGroup,
    HostCategory,
    HostSeverity,
    HostTemplate,
    Service,
    ServiceGroup,
    Command,
    MonitoringServer,
]
MODELS_MIXIN_LIST: dict[str, type[ListMixin]] = {model.model_type: model for model in _list_models}

_create_models: list[type[CreateMixin]] = [
    Host,
    HostGroup,
    HostCategory,
    HostSeverity,
    HostTemplate,
    Service,
    ServiceGroup,
    Command,
]
MODELS_MIXIN_CREATE: dict[str, type[CreateMixin]] = {
    model.model_type: model for model in _create_models
}

_update_models: list[type[UpdateMixin]] = [
    Host,
    HostGroup,
    HostCategory,
    HostSeverity,
    HostTemplate,
    Service,
]
MODELS_MIXIN_UPDATE: dict[str, type[UpdateMixin]] = {
    model.model_type: model for model in _update_models
}


_delete_models: list[type[DeleteMixin]] = [
    Host,
    HostGroup,
    HostCategory,
    HostSeverity,
    HostTemplate,
    Service,
    ServiceGroup,
]
MODELS_MIXIN_DELETE: dict[str, type[DeleteMixin]] = {
    model.model_type: model for model in _delete_models
}
