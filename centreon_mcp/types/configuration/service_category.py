from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder, BaseParams
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin

DESCRIPTION = {
    "name": "Name for this service category",
    "alias": "Alias for this service category",
    "is_activated": "Whether this service category is enabled or not",
}


class ServiceCategoryOrder(BaseOrder):
    model_type: Literal["service_category"] = "service_category"

    field: Literal["id", "name", "alias", "is_activated"] = "name"


class ServiceCategoryFilter(BaseFilter):
    model_type: Literal["service_category"] = "service_category"

    service_category_id: int | None = Field(default=None, serialization_alias="id $eq")
    service_category_name: str | None = Field(default=None, serialization_alias="name $eq")
    service_category_alias: str | None = Field(default=None, serialization_alias="alias $eq")
    service_category_is_activated: bool | None = Field(
        default=None, serialization_alias="is_activated $eq"
    )
    host_id: int | None = Field(default=None, serialization_alias="host.id $eq")
    host_name: str | None = Field(default=None, serialization_alias="host.name $eq")
    host_group_id: int | None = Field(default=None, serialization_alias="hostgroup.id $eq")
    host_group_name: str | None = Field(default=None, serialization_alias="hostgroup.name $eq")
    host_category_id: int | None = Field(default=None, serialization_alias="hostcategory.id $eq")
    host_category_name: str | None = Field(
        default=None, serialization_alias="hostcategory.name $eq"
    )
    service_group_id: int | None = Field(default=None, serialization_alias="servicegroup.id $eq")
    service_group_name: str | None = Field(
        default=None, serialization_alias="servicegroup.name $eq"
    )


class ServiceCategoryBaseParams(BaseParams):
    model_type: Literal["service_category"] = "service_category"

    is_activated: bool = Field(default=True, description=DESCRIPTION["is_activated"])


class ServiceCategoryFullParams(ServiceCategoryBaseParams):
    name: str = Field(description=DESCRIPTION["name"])
    alias: str = Field(description=DESCRIPTION["alias"])


class ServiceCategory(
    BaseModel,
    CreateMixin[ServiceCategoryFullParams],
    ListMixin[ServiceCategoryFilter, ServiceCategoryOrder],
    DeleteMixin,
):
    endpoint: ClassVar[str] = "configuration/services/categories"
    model_type: ClassVar[str] = "service_category"

    id: int
    name: str
    alias: str
    is_activated: bool
