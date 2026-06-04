from typing import ClassVar

from pydantic import AliasPath, BaseModel, Field, field_validator

from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, ReadMixin, UpdateMixin

DESCRIPTION = {
    "name": "Host group name",
    "alias": "Host group alias",
    "icon_id": "Define the image ID that should be associated with this host group",
    "geo_coords": "Geographical coordinates use by Centreon Map module to position element on map",
    "comment": "Comments on this host group",
    "hosts": "Hosts linked to this host group",
}


class HostGroup(BaseModel, ListMixin):
    endpoint: ClassVar[str] = "monitoring/hostgroups"

    id: int
    name: str


class HostGroupConfigurationBaseParams(BaseModel):
    alias: str | None = Field(None, description=DESCRIPTION["alias"])
    icon_id: int | None = Field(None, description=DESCRIPTION["icon_id"])
    geo_coords: str | None = Field(None, description=DESCRIPTION["geo_coords"])
    comment: str | None = Field(None, description=DESCRIPTION["comment"])
    hosts: list[int] | None = Field(None, description=DESCRIPTION["hosts"])


class HostGroupConfigurationPartialParams(HostGroupConfigurationBaseParams):
    name: str | None = Field(None, description=DESCRIPTION["name"])


class HostGroupConfigurationFullParams(HostGroupConfigurationBaseParams):
    name: str = Field(description=DESCRIPTION["name"])


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
    icon_id: int | None = Field(None, validation_alias=AliasPath("icon", "id"))
    geo_coords: str | None = None
    comment: str | None = None
    is_activated: bool
    enabled_hosts_count: int | None = None
    disabled_hosts_count: int | None = None
    hosts: list[int] = Field(default_factory=list)

    @field_validator("hosts", mode="before")
    @classmethod
    def validate_hosts(cls, hosts: list[dict]) -> list[int]:
        """
        Convert list of Link to list of int to be aligned with params.
        """
        return [host["id"] for host in hosts]
