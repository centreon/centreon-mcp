from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel

from centreon_mcp.utils.mixins import ListMixin


class MonitoringServer(BaseModel, ListMixin):
    endpoint: ClassVar[str] = "monitoring/servers"

    id: int
    name: str
    address: str | None = None
    description: str | None = None
    is_running: bool
    last_alive: int | None = None
    version: str | None = None


class MonitoringServerConfiguration(BaseModel, ListMixin):
    endpoint: ClassVar[str] = "configuration/monitoring-servers"

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
    centreonbroker_cfg_path: str
    centreonbroker_module_path: str
    centreonbroker_logs_path: str
    centreonconnector_path: str
    init_script_centreontrapd: str
    snmp_trapd_path_conf: str
    remote_id: int | None = None
    remote_server_use_as_proxy: bool
    is_updated: bool
    is_activate: bool
