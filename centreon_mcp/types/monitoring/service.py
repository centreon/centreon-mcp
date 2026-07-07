from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, StatusCount
from centreon_mcp.utils.request import request


class ServiceFilter(BaseFilter):
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


class ServiceStatusCount(StatusCount):
    critical: int
    unknown: int
    ok: int
    warning: int


class Service(BaseModel):
    @staticmethod
    async def count_by_status(search: str | None) -> ServiceStatusCount:
        """
        Count services by status.
        """
        params = {"search": search}
        content = await request("GET", "monitoring/services/status", params=params)
        return ServiceStatusCount(**content)
