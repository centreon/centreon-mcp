from typing import ClassVar, Literal

from pydantic import Field

from centreon_mcp.types.monitoring.status.base import BaseStatusCount
from centreon_mcp.utils.base import BaseFilter
from centreon_mcp.utils.mixins import CountMixin


class HostStatusCountFilter(BaseFilter):
    model_type: Literal["host"] = "host"

    host_group_id: int | None = Field(default=None, serialization_alias="host_group.id $eq")
    host_group_name: str | None = Field(default=None, serialization_alias="host_group.name $eq")
    host_category_id: int | None = Field(default=None, serialization_alias="host_category.id $eq")
    host_category_name: str | None = Field(
        default=None, serialization_alias="host_category.name $eq"
    )


class HostStatusCount(BaseStatusCount, CountMixin[HostStatusCountFilter]):
    endpoint: ClassVar[str] = "monitoring/hosts/status"
    model_type: ClassVar[str] = "host"

    total: int
    pending: int
    up: int
    down: int
    unreachable: int
