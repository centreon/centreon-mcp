from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.types.base import BaseFilter, BaseOrder, HostState
from centreon_mcp.utils.mixins import ListMixin


class HostGroupOrder(BaseOrder):
    field: Literal["name", "host.name", "host.alias", "host.address", "host.state"] = "host.name"


class HostGroupFilter(BaseFilter):
    host_id: int | None = Field(None, serialization_alias="host.id $eq")
    host_name: str | None = Field(None, serialization_alias="host.name $eq")
    host_alias: str | None = Field(None, serialization_alias="host.alias $eq")
    host_address: str | None = Field(None, serialization_alias="host.address $eq")
    host_state: HostState | None = Field(None, serialization_alias="host.state $eq")
    poller_id: int | None = Field(None, serialization_alias="poller.id $eq")
    host_group_id: int | None = Field(None, serialization_alias="id $eq")
    host_group_name: str | None = Field(None, serialization_alias="name $eq")


class HostGroup(BaseModel, ListMixin[HostGroupFilter, HostGroupOrder]):
    endpoint: ClassVar[str] = "monitoring/hostgroups"

    id: int
    name: str
