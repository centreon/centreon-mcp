from typing import ClassVar

from pydantic import BaseModel, Field

from centreon_mcp.types.base import Link
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, ReadMixin, UpdateMixin

DESCRIPTION = {
    "name": "Host group name",
    "alias": "Host group alias",
    "icon_id": "Define the image ID that should be associated with this host group",
    "geo_coords": "Geographical coordinates use by Centreon Map module to position element on map",
    "comment": "Comments on this host group",
    "hosts": "Hosts linked to this host group",
    "hosts_added": "Ids of the hosts to add to the host group.",
    "hosts_removed": "Ids of the hosts to remove from the host group.",
}


class Icon(BaseModel):
    id: int
    name: str
    url: str


class HostGroup(BaseModel, ListMixin):
    endpoint: ClassVar[str] = "monitoring/hostgroups"

    id: int
    name: str


class HostGroupConfigurationBaseParams(BaseModel):
    alias: str | None = Field(None, description=DESCRIPTION["alias"])
    icon_id: int | None = Field(None, description=DESCRIPTION["icon_id"])
    geo_coords: str | None = Field(None, description=DESCRIPTION["geo_coords"])
    comment: str | None = Field(None, description=DESCRIPTION["comment"])


class HostGroupConfigurationPartialParams(HostGroupConfigurationBaseParams):
    name: str | None = Field(None, description=DESCRIPTION["name"])
    hosts_added: list[int] = Field(default_factory=list, description=DESCRIPTION["hosts_added"])
    hosts_removed: list[int] = Field(default_factory=list, description=DESCRIPTION["hosts_removed"])


class HostGroupConfigurationFullParams(HostGroupConfigurationBaseParams):
    name: str = Field(description=DESCRIPTION["name"])
    hosts: list[int] | None = Field(None, description=DESCRIPTION["hosts"])


class HostGroupConfiguration(
    BaseModel,
    CreateMixin[HostGroupConfigurationFullParams],
    UpdateMixin[HostGroupConfigurationFullParams],
    DeleteMixin,
    ReadMixin,
    ListMixin,
):
    endpoint: ClassVar[str] = "configuration/hosts/groups"

    id: int
    name: str
    alias: str | None = None
    icon: Icon | None = None
    geo_coords: str | None = None
    comment: str | None = None
    is_activated: bool
    enabled_hosts_count: int | None = None
    disabled_hosts_count: int | None = None
    hosts: list[Link] = Field(default_factory=list)
