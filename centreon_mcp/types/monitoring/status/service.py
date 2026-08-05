from typing import ClassVar, Literal

from pydantic import Field

from centreon_mcp.types.monitoring.status.base import BaseStatusCount
from centreon_mcp.utils.base import BaseFilter
from centreon_mcp.utils.mixins import CountMixin


class ServiceStatusCountFilter(BaseFilter):
    model_type: Literal["service"] = "service"

    host_name: str | None = Field(default=None, serialization_alias="host.name $eq")
    host_group_id: int | None = Field(default=None, serialization_alias="host_group.id $eq")
    host_group_name: str | None = Field(default=None, serialization_alias="host_group.name $eq")
    host_category_id: int | None = Field(default=None, serialization_alias="host_category.id $eq")
    host_category_name: str | None = Field(
        default=None, serialization_alias="host_category.name $eq"
    )
    service_group_id: int | None = Field(default=None, serialization_alias="service_group.id $eq")
    service_group_name: str | None = Field(
        default=None, serialization_alias="service_group.name $eq"
    )
    service_category_id: int | None = Field(
        default=None, serialization_alias="service_category.id $eq"
    )
    service_category_name: str | None = Field(
        default=None, serialization_alias="service_category.name $eq"
    )


class ServiceStatusCount(BaseStatusCount, CountMixin[ServiceStatusCountFilter]):
    endpoint: ClassVar[str] = "monitoring/services/status"
    model_type: ClassVar[str] = "service"

    total: int
    pending: int
    critical: int
    unknown: int
    ok: int
    warning: int
