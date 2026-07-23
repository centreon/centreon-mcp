from typing import Literal

from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, StatusCount
from centreon_mcp.utils.request import request


class HostFilter(BaseFilter):
    model_type: Literal["host"] = "host"

    host_group_id: int | None = Field(default=None, serialization_alias="host_group.id $eq")
    host_group_name: str | None = Field(default=None, serialization_alias="host_group.name $eq")
    host_category_id: int | None = Field(default=None, serialization_alias="host_category.id $eq")
    host_category_name: str | None = Field(
        default=None, serialization_alias="host_category.name $eq"
    )


class HostStatusCount(StatusCount):
    up: int
    down: int
    unreachable: int


class Host(BaseModel):
    @staticmethod
    async def count_by_status(search: str | None) -> HostStatusCount:
        """
        Count hosts by status.
        """
        params = {"search": search}
        content = await request("GET", "monitoring/hosts/status", params=params)
        return HostStatusCount(**content)
