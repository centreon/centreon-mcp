from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.types.base import BaseFilter, BaseOrder
from centreon_mcp.utils.mixins import ListMixin


class MonitoringServerOrder(BaseOrder):
    field: Literal["id", "name", "running"] = "name"


class MonitoringServerFilter(BaseFilter):
    monitoring_server_id: int | None = Field(None, serialization_alias="id $eq")
    monitoring_server_name: str | None = Field(None, serialization_alias="name $eq")
    monitoring_server_running: bool | None = Field(None, serialization_alias="running $eq")


class MonitoringServer(BaseModel, ListMixin[MonitoringServerFilter, MonitoringServerOrder]):
    endpoint: ClassVar[str] = "monitoring/servers"

    id: int
    name: str
    address: str | None = None
    description: str | None = None
    is_running: bool
    last_alive: int | None = None
    version: str | None = None
