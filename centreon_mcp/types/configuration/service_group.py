from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder, BaseParams
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin

DESCRIPTION = {
    "name": "Service group name",
    "alias": "Service group alias",
    "geo_coords": "Geographical coordinates use by Centreon Map module to position element on map",
    "comment": "Comments on this service group",
    "is_activated": "Indicates whether the service group is activated or not",
}


class ServiceGroupOrder(BaseOrder):
    model_type: Literal["service_group"] = "service_group"

    field: Literal["id", "name", "alias", "is_activated"] = "name"


class ServiceGroupFilter(BaseFilter):
    model_type: Literal["service_group"] = "service_group"

    service_group_id: int | None = Field(default=None, serialization_alias="id $eq")
    service_group_name: str | None = Field(default=None, serialization_alias="name $eq")
    service_group_alias: str | None = Field(default=None, serialization_alias="alias $eq")
    service_group_is_activated: bool | None = Field(
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
    service_category_id: int | None = Field(
        default=None, serialization_alias="servicecategory.id $eq"
    )
    service_category_name: str | None = Field(
        default=None, serialization_alias="servicecategory.name $eq"
    )


class ServiceGroupBaseParams(BaseParams):
    model_type: Literal["service_group"] = "service_group"

    geo_coords: str | None = Field(
        default=None, max_length=32, description=DESCRIPTION["geo_coords"]
    )
    comment: str | None = Field(default=None, max_length=65535, description=DESCRIPTION["comment"])
    is_activated: bool = Field(default=True, description=DESCRIPTION["is_activated"])


class ServiceGroupFullParams(ServiceGroupBaseParams):
    alias: str = Field(max_length=200, description=DESCRIPTION["alias"])
    name: str = Field(max_length=200, description=DESCRIPTION["name"])


class ServiceGroup(
    BaseModel,
    CreateMixin[ServiceGroupFullParams],
    DeleteMixin,
    ListMixin[ServiceGroupFilter, ServiceGroupOrder],
):
    endpoint: ClassVar[str] = "configuration/services/groups"
    model_type: ClassVar[str] = "service_group"

    id: int
    name: str
    alias: str | None = None
    geo_coords: str | None = None
    comment: str | None = None
    is_activated: bool
