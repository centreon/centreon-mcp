from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, ReadMixin, UpdateMixin

DESCRIPTION = {
    "name": "Name for this host category",
    "alias": "Alias for this host category",
    "comment": "Comment for this host category",
    "is_activated": "Whether this host category is enabled or not",
}


class HostCategoryConfigurationOrder(BaseOrder):
    field: Literal["id", "name", "alias", "is_activated"] = "name"


class HostCategoryConfigurationFilter(BaseFilter):
    host_category_id: int | None = Field(None, serialization_alias="id $eq")
    host_category_name: str | None = Field(None, serialization_alias="name $eq")
    host_category_alias: str | None = Field(None, serialization_alias="alias $eq")
    host_category_is_activated: bool | None = Field(None, serialization_alias="is_activated $eq")


class HostCategoryConfigurationBaseParams(BaseModel):
    is_activated: bool | None = Field(None, description=DESCRIPTION["is_activated"])
    comment: str | None = Field(None, description=DESCRIPTION["comment"])


class HostCategoryConfigurationPartialParams(HostCategoryConfigurationBaseParams):
    name: str | None = Field(None, description=DESCRIPTION["name"])
    alias: str | None = Field(None, description=DESCRIPTION["alias"])


class HostCategoryConfigurationFullParams(HostCategoryConfigurationBaseParams):
    name: str = Field(description=DESCRIPTION["name"])
    alias: str = Field(description=DESCRIPTION["alias"])


class HostCategoryConfiguration(
    BaseModel,
    CreateMixin[HostCategoryConfigurationFullParams],
    UpdateMixin[HostCategoryConfigurationFullParams],
    DeleteMixin,
    ReadMixin,
    ListMixin,
):
    endpoint: ClassVar[str] = "configuration/hosts/categories"

    id: int
    name: str
    alias: str
    is_activated: bool
    comment: str | None = None
