from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.types.monitoring.servicegroup import (
    ServiceGroup,
    ServiceGroupFilter,
    ServiceGroupOrder,
)
from centreon_mcp.utils import logger

servicegroup = FastMCP()


@servicegroup.tool(
    annotations={
        "title": "List service groups in real-time monitoring",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_servicegroups(
    filters: list[ServiceGroupFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: ServiceGroupOrder | None = None,
) -> list[ServiceGroup]:
    """
    List service groups in real-time monitoring matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all services groups except if explicitly intended.
    """
    logger.info("Executing tool list_servicegroups")
    return await ServiceGroup.list(filters, limit, page, order)
