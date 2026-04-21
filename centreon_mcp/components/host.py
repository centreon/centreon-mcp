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
    Count hosts by status in real-time monitoring.
    Returns the total number of hosts in each state: UP, DOWN, UNREACHABLE, and PENDING.
    Each filter object narrows results by host group or host category.
    Fields within a single filter are ANDed together, multiple filter objects are ORed.
    Omit filters to count all hosts.
    Use this tool instead of list_resources when only aggregate counts are needed
    """
    logger.info("Executing tool count_hosts_by_status")
    search = json.dumps(HostFilter.join(filters))
    return await Host.count_by_status(search)
