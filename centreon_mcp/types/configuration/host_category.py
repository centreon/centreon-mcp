from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder, BaseParams
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, PutMixin, ReadMixin

DESCRIPTION = {
    "name": "Name for this host category",
    "alias": "Alias for this host category",
    "comment": "Comment for this host category",
    "is_activated": "Whether this host category is enabled or not",
}


class HostCategoryOrder(BaseOrder):
    model_type: Literal["host_category"] = "host_category"

    field: Literal["id", "name", "alias", "is_activated"] = "name"


class HostCategoryFilter(BaseFilter):
    model_type: Literal["host_category"] = "host_category"

    host_category_id: int | None = Field(default=None, serialization_alias="id $eq")
    host_category_name: str | None = Field(default=None, serialization_alias="name $eq")
    host_category_alias: str | None = Field(default=None, serialization_alias="alias $eq")
    host_category_is_activated: bool | None = Field(
        default=None, serialization_alias="is_activated $eq"
    )


class HostCategoryBaseParams(BaseParams):
    model_type: Literal["host_category"] = "host_category"

    is_activated: bool | None = Field(default=None, description=DESCRIPTION["is_activated"])
    comment: str | None = Field(default=None, description=DESCRIPTION["comment"])


class HostCategoryPartialParams(HostCategoryBaseParams):
    name: str | None = Field(default=None, description=DESCRIPTION["name"])
    alias: str | None = Field(default=None, description=DESCRIPTION["alias"])


class HostCategoryFullParams(HostCategoryBaseParams):
    name: str = Field(description=DESCRIPTION["name"])
    alias: str = Field(description=DESCRIPTION["alias"])


class HostCategory(
    BaseModel,
    CreateMixin[HostCategoryFullParams],
    PutMixin[HostCategoryPartialParams, HostCategoryFullParams],
    DeleteMixin,
    ReadMixin,
    ListMixin[HostCategoryFilter, HostCategoryOrder],
):
    endpoint: ClassVar[str] = "configuration/hosts/categories"
    model_type: ClassVar[str] = "host_category"
    full_params_cls: ClassVar[type[HostCategoryFullParams]] = HostCategoryFullParams

    id: int
    name: str
    alias: str
    is_activated: bool
    comment: str | None = None
