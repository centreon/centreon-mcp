from typing import ClassVar

from pydantic import BaseModel, Field

from centreon_mcp.types.base import CentreonBaseModel
from centreon_mcp.utils.request import request

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


class Host(BaseModel):
    id: int
    name: str


class Icon(BaseModel):
    id: int
    name: str
    url: str


class HostGroup(CentreonBaseModel):
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


class HostGroupConfiguration(CentreonBaseModel):
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
    hosts: list[Host] = Field(default_factory=list)

    @classmethod
    async def get(cls, host_group_id: int) -> "HostGroupConfiguration":
        """
        Get a host group.
        """
        content = await request("GET", f"{cls.endpoint}/{host_group_id}")
        return cls(**content)

    @classmethod
    async def update(cls, hostgroup_id: int, params: HostGroupConfigurationFullParams) -> bool:
        """
        Update a host group.
        Return True if successful; otherwise, raise an exception.
        """
        payload = params.model_dump(mode="json", exclude_none=True)
        await request("PUT", f"{cls.endpoint}/{hostgroup_id}", payload)
        return True

    @classmethod
    async def delete(cls, hostgroup_id: int) -> bool:
        """
        Delete a host group.
        Return True if successful; otherwise, raise an exception.
        """
        await request("DELETE", f"{cls.endpoint}/{hostgroup_id}")
        return True
