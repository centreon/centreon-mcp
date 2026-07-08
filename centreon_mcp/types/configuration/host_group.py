from typing import ClassVar, Literal

from pydantic import AliasPath, BaseModel, Field, field_validator

from centreon_mcp.utils.base import BaseFilter, BaseOrder
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, PutMixin, ReadMixin

DESCRIPTION = {
    "name": "Host group name",
    "alias": "Host group alias",
    "icon_id": "Define the image ID that should be associated with this host group",
    "geo_coords": "Geographical coordinates use by Centreon Map module to position element on map",
    "comment": "Comments on this host group",
    "hosts": "Hosts linked to this host group",
}


class HostGroupConfigurationOrder(BaseOrder):
    model_type: Literal["host_group"] = "host_group"

    field: Literal["id", "name", "alias", "is_activated"] = "name"


class HostGroupConfigurationFilter(BaseFilter):
    model_type: Literal["host_group"] = "host_group"

    host_group_id: int | None = Field(default=None, serialization_alias="id $eq")
    host_group_name: str | None = Field(default=None, serialization_alias="name $eq")
    host_group_alias: str | None = Field(default=None, serialization_alias="alias $eq")
    host_group_is_activated: bool | None = Field(
        default=None, serialization_alias="is_activated $eq"
    )


class HostGroupConfigurationBaseParams(BaseModel):
    model_type: Literal["host_group"] = "host_group"

    alias: str | None = Field(default=None, description=DESCRIPTION["alias"])
    icon_id: int | None = Field(default=None, description=DESCRIPTION["icon_id"])
    geo_coords: str | None = Field(default=None, description=DESCRIPTION["geo_coords"])
    comment: str | None = Field(default=None, description=DESCRIPTION["comment"])
    hosts: list[int] | None = Field(default=None, description=DESCRIPTION["hosts"])


class HostGroupConfigurationPartialParams(HostGroupConfigurationBaseParams):
    name: str | None = Field(default=None, description=DESCRIPTION["name"])


class HostGroupConfigurationFullParams(HostGroupConfigurationBaseParams):
    name: str = Field(description=DESCRIPTION["name"])


class HostGroupConfiguration(
    BaseModel,
    CreateMixin[HostGroupConfigurationFullParams],
    PutMixin[HostGroupConfigurationPartialParams, HostGroupConfigurationFullParams],
    DeleteMixin,
    ReadMixin,
    ListMixin[HostGroupConfigurationFilter, HostGroupConfigurationOrder],
):
    endpoint: ClassVar[str] = "configuration/hosts/groups"
    model_type: ClassVar[str] = "host_group"
    full_params_cls: ClassVar[type[HostGroupConfigurationFullParams]] = (
        HostGroupConfigurationFullParams
    )

    id: int
    name: str
    alias: str | None = None
    icon_id: int | None = Field(default=None, validation_alias=AliasPath("icon", "id"))
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
