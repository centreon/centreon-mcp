from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder, HostState
from centreon_mcp.utils.mixins import ListMixin


class ServiceGroupOrder(BaseOrder):
    field: Literal[
        "name",
        "host.name",
        "host.alias",
        "host.address",
        "host.state",
        "service.name",
        "service.display_name",
    ] = "name"


class ServiceGroupFilter(BaseFilter):
    host_id: int | None = Field(default=None, serialization_alias="host.id $eq")
    host_name: str | None = Field(default=None, serialization_alias="host.name $eq")
    host_alias: str | None = Field(default=None, serialization_alias="host.alias $eq")
    host_address: str | None = Field(default=None, serialization_alias="host.address $eq")
    host_state: HostState | None = Field(default=None, serialization_alias="host.state $eq")
    poller_id: int | None = Field(default=None, serialization_alias="poller.id $eq")
    host_group_id: int | None = Field(default=None, serialization_alias="host_group.id $eq")
    service_group_id: int | None = Field(default=None, serialization_alias="id $eq")
    service_group_name: str | None = Field(default=None, serialization_alias="name $eq")
    service_name: str | None = Field(default=None, serialization_alias="service.name $eq")
    service_display_name: str | None = Field(
        default=None, serialization_alias="service.display_name $eq"
    )
    host_group_name: str | None = Field(default=None, serialization_alias="host_group.name $eq")


class ServiceGroup(BaseModel, ListMixin[ServiceGroupFilter, ServiceGroupOrder]):
    endpoint: ClassVar[str] = "monitoring/servicegroups"

    id: int
    name: str
