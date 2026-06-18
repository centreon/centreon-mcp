import json

from fastmcp import FastMCP

from centreon_mcp.types.monitoring.service import Service, ServiceFilter, ServiceStatusCount
from centreon_mcp.utils import logger

service = FastMCP()


@service.tool(
    annotations={
        "title": "Count services by status in real-time monitoring",
        "readOnlyHint": True,
        "destructiveHint": False,
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
