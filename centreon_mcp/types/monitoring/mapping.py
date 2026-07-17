from centreon_mcp.types.monitoring.host_group import HostGroup
from centreon_mcp.types.monitoring.monitoring_server import MonitoringServer
from centreon_mcp.types.monitoring.servicegroup import ServiceGroup
from centreon_mcp.utils.mixins import ListMixin

_list_models: list[type[ListMixin]] = [
    HostGroup,
    ServiceGroup,
    MonitoringServer,
]
MODELS_MIXIN_LIST: dict[str, type[ListMixin]] = {model.model_type: model for model in _list_models}
