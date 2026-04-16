import json

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseFilter
from centreon_mcp.utils.type import Host, HostStatusCount

host = FastMCP()


class HostFilter(BaseFilter):
    host_group_id: int | None = Field(None, serialization_alias="host_group.id $eq")
    host_group_name: str | None = Field(None, serialization_alias="host_group.name $eq")
    host_category_id: int | None = Field(
        None, serialization_alias="host_category.id $eq"
    )
    host_category_name: str | None = Field(
        None, serialization_alias="host_category.name $eq"
    )


@host.tool(
    annotations={
        "title": "Count hosts by status in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def count_hosts_by_status(
    filters: list[HostFilter] | None = None,
) -> HostStatusCount:
    """
    Count hosts by status in real-time monitoring matching the given filters.
    """
    logger.info("Executing tool count_hosts_by_status")
    conditions = (
        {
            "$or": [
                {"$and": filter.conditions} for filter in filters if filter.conditions
            ]
        }
        if filters
        else {}
    )
    return await Host.count_by_status(search=json.dumps(conditions))
