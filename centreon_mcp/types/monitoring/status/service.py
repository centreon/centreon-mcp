from typing import ClassVar, Literal

from pydantic import Field

from centreon_mcp.types.monitoring.status.base import BaseStatusCount
from centreon_mcp.utils.base import BaseFilter
from centreon_mcp.utils.mixins import CountMixin


class ServiceStatusCountFilter(BaseFilter):
    model_type: Literal["service"] = "service"

    host_name: str | None = Field(default=None, serialization_alias="host.name $lk")
    host_group_id: int | None = Field(default=None, serialization_alias="host_group.id $eq")
    host_group_name: str | None = Field(default=None, serialization_alias="host_group.name $lk")
    host_category_id: int | None = Field(default=None, serialization_alias="host_category.id $eq")
    host_category_name: str | None = Field(
        default=None, serialization_alias="host_category.name $lk"
    )
    service_group_id: int | None = Field(default=None, serialization_alias="service_group.id $eq")
    service_group_name: str | None = Field(
        default=None, serialization_alias="service_group.name $lk"
    )
    service_category_id: int | None = Field(
        default=None, serialization_alias="service_category.id $eq"
    )
    service_category_name: str | None = Field(
        default=None, serialization_alias="service_category.name $lk"
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
