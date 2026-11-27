from datetime import datetime
from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder, ResourceType, Status
from centreon_mcp.utils.mixins import ListMixin

# A resource is either a host or a service. A service always belongs to exactly one host, which is
# its parent; a host has no parent. These descriptions are the only documentation the LLM client
# sees, so they spell out which name goes in which field.
DESCRIPTION = {
    "resource_name": (
        "The resource's own name. For a host, the host name (e.g. 'srv-web-01'). For a service, "
        "the service name only (e.g. 'CPU', 'Ping', 'Disk-/var'), never the name of the host it "
        "runs on: that goes in `resource_parent_name`."
    ),
    "resource_alias": (
        "The host alias, a free-text label set on a host in addition to its name "
        "(e.g. 'Production web server'). Only hosts have an alias, so this field never matches "
        "a service. To find a host by its name, use `resource_name` instead."
    ),
    "resource_parent_name": (
        "The name of the host a service belongs to. Only services have a parent (their host); "
        "hosts have none, so setting this field returns services only. "
        "Example: {'resource_parent_name': 'srv-web-01'} returns the services of host "
        "'srv-web-01'. Never put a service name here: it goes in `resource_name`."
    ),
    "information_like": (
        "The resource output (plugin information) to match, e.g. '%timeout%' for outputs "
        "containing 'timeout'."
    ),
    "information_unlike": (
        "The resource output (plugin information) to exclude, e.g. '%timeout%' to drop outputs "
        "containing 'timeout'."
    ),
}


class ResourceOrder(BaseOrder):
    model_type: Literal["resource"] = "resource"

    field: Literal["host.name", "host.alias", "host.address", "host.state"] = "host.name"


class ResourceFilter(BaseFilter):
    model_type: Literal["resource"] = "resource"

    # Fields available for filtering in Centreon API
    resource_name: str | None = Field(
        default=None,
        serialization_alias="name $lk",
        description=DESCRIPTION["resource_name"],
    )
    resource_alias: str | None = Field(
        default=None,
        serialization_alias="alias $lk",
        description=DESCRIPTION["resource_alias"],
    )
    resource_parent_name: str | None = Field(
        default=None,
        serialization_alias="parent_name $lk",
        description=DESCRIPTION["resource_parent_name"],
    )
    information_like: str | None = Field(
        default=None,
        serialization_alias="information $lk",
        description=DESCRIPTION["information_like"],
    )
    information_unlike: str | None = Field(
        default=None,
        serialization_alias="information $nk",
        description=DESCRIPTION["information_unlike"],
    )


class ResourceParent(BaseModel):
    id: int
    name: str
    type: ResourceType
    alias: str | None = None
    fqdn: str | None = None


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
    parent: ResourceParent | None = None
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
