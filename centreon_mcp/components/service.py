import json

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseFilter
from centreon_mcp.utils.type import Service, ServiceStatusCount

service = FastMCP()


class ServiceFilter(BaseFilter):
    host_name: str | None = Field(None, serialization_alias="host.name $eq")
    host_group_id: int | None = Field(None, serialization_alias="host_group.id $eq")
    host_group_name: str | None = Field(None, serialization_alias="host_group.name $eq")
    host_category_id: int | None = Field(None, serialization_alias="host_category.id $eq")
    host_category_name: str | None = Field(None, serialization_alias="host_category.name $eq")
    service_group_id: int | None = Field(None, serialization_alias="service_group.id $eq")
    service_group_name: str | None = Field(None, serialization_alias="service_group.name $eq")
    service_category_id: int | None = Field(None, serialization_alias="service_category.id $eq")
    service_category_name: str | None = Field(None, serialization_alias="service_category.name $eq")


@service.tool(
    annotations={
        "title": "Count services by status in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def count_services_by_status(
    filters: list[ServiceFilter] | None = None,
) -> ServiceStatusCount:
    """
    Count services by status in real-time monitoring.
    Returns the total number of services in each state: OK, WARNING, CRITICAL, UNKNOWN and PENDING.
    Each filter object narrows results by host group, host category, service group, service category or host.
    Fields within a single filter are ANDed together, multiple filter objects are ORed.
    Omit filters to count all services.
    Use this tool instead of list_resources when only aggregate counts are needed
    """
    logger.info("Executing tool count_services_by_status")
    search = json.dumps(ServiceFilter.join(filters))
    return await Service.count_by_status(search)
