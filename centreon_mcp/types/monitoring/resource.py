from datetime import datetime
from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.types.base import BaseFilter, BaseOrder, ResourceType, Status
from centreon_mcp.utils.mixins import ListMixin


class ResourceOrder(BaseOrder):
    field: Literal["host.name", "host.alias", "host.address", "host.state"] = "host.name"


class ResourceFilter(BaseFilter):
    # Fields available for filtering in Centreon API
    name: str | None = Field(
        None,
        serialization_alias="name $lk",
        description="Name of the resource (host or service)",
    )
    alias: str | None = Field(
        None,
        serialization_alias="alias $lk",
        description="Alias of the resource (host or service)",
    )
    parent_name: str | None = Field(
        None,
        serialization_alias="parent_name $lk",
        description="Name of the parent resource (host or service)",
    )
    information_like: str | None = Field(
        None,
        serialization_alias="information $lk",
        description="Filter resources whose output/information contains this string (case-insensitive substring match)",
    )
    information_unlike: str | None = Field(
        None,
        serialization_alias="information $nk",
        description="Filter resources whose output/information does not contain this string (case-insensitive substring exclusion)",
    )


class Resource(BaseModel, ListMixin[ResourceFilter, ResourceOrder]):
    endpoint: ClassVar[str] = "monitoring/resources"

    uuid: str
    id: int
    type: ResourceType
    name: str
    alias: str | None = None
    fqdn: str | None = None
    host_id: int
    service_id: int | None = None
    monitoring_server_name: str
    is_in_downtime: bool
    is_acknowledged: bool
    is_in_flapping: bool
    status: Status
    information: str | None = None
    has_active_checks_enabled: bool
    has_passive_checks_enabled: bool
    last_status_change: datetime | None = None
    last_check: str | None = None
    tries: str | None = None
