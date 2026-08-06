from datetime import datetime
from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder
from centreon_mcp.utils.mixins import ListMixin
from centreon_mcp.utils.request import request


class MonitoringServerOrder(BaseOrder):
    model_type: Literal["monitoring_server"] = "monitoring_server"

    field: Literal["id", "name"] = "name"


class MonitoringServerFilter(BaseFilter):
    model_type: Literal["monitoring_server"] = "monitoring_server"

    monitoring_server_id: int | None = Field(default=None, serialization_alias="id $eq")
    monitoring_server_name: str | None = Field(default=None, serialization_alias="name $eq")


class MonitoringServer(BaseModel, ListMixin[MonitoringServerFilter, MonitoringServerOrder]):
    endpoint: ClassVar[str] = "configuration/monitoring-servers"
    model_type: ClassVar[str] = "monitoring_server"

    id: int
    name: str
    address: str
    is_localhost: bool
    is_default: bool
    ssh_port: int
    last_restart: datetime | None = None
    engine_start_command: str
    engine_stop_command: str
    engine_restart_command: str
    engine_reload_command: str
    nagios_bin: str
    nagiostats_bin: str
    broker_reload_command: str
    centreonbroker_cfg_path: str | None = None
    centreonbroker_module_path: str | None = None
    centreonbroker_logs_path: str | None = None
    centreonconnector_path: str | None = None
    init_script_centreontrapd: str
    snmp_trapd_path_conf: str
    remote_id: int | None = None
    remote_server_use_as_proxy: bool
    is_updated: bool
    is_activate: bool

    @classmethod
    async def manage(
        cls, action: Literal["generate", "reload"], monitoring_server_id: int | None = None
    ) -> bool:
        """
        Generate/Reload the configuration of a monitoring server based on its id if provided.
        Else, generate/reload configuration of all monitoring servers.
        Return True if successful; otherwise, raise an exception.
        """
        endpoint = (
            f"{cls.endpoint}/{monitoring_server_id}/{action}"
            if monitoring_server_id is not None
            else f"{cls.endpoint}/{action}"
        )
        await request("GET", endpoint)
        return True
