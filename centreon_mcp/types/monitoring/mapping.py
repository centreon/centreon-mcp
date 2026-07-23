from centreon_mcp.types.monitoring.actions.acknowledgement import Acknowledgement
from centreon_mcp.types.monitoring.actions.check import Check
from centreon_mcp.types.monitoring.actions.comment import Comment
from centreon_mcp.types.monitoring.actions.downtime import Downtime
from centreon_mcp.types.monitoring.host_group import HostGroup
from centreon_mcp.types.monitoring.monitoring_server import MonitoringServer
from centreon_mcp.types.monitoring.servicegroup import ServiceGroup
from centreon_mcp.utils.mixins import ListMixin, SetMixin

_list_models: list[type[ListMixin]] = [
    HostGroup,
    ServiceGroup,
    MonitoringServer,
    Acknowledgement,
    Downtime,
]
MODELS_MIXIN_LIST: dict[str, type[ListMixin]] = {model.model_type: model for model in _list_models}


_set_models: list[type[SetMixin]] = [Acknowledgement, Downtime, Check, Comment]
MODELS_MIXIN_SET: dict[str, type[SetMixin]] = {model.model_type: model for model in _set_models}
