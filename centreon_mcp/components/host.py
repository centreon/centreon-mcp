import json

from fastmcp import FastMCP

from centreon_mcp.types.monitoring.host import Host, HostFilter, HostStatusCount
from centreon_mcp.utils import logger

host = FastMCP()


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
