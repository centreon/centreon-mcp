from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.components.base import _list
from centreon_mcp.types.monitoring.host_group import HostGroup, HostGroupFilter, HostGroupOrder
from centreon_mcp.utils import logger

host_group = FastMCP()


@host_group.tool(
    annotations={
        "title": "List host groups in real-time monitoring",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_host_groups(
    filters: list[HostGroupFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: HostGroupOrder | None = None,
) -> list[HostGroup]:
    """
    List host groups in real-time monitoring matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all host groups except if explicitly intended.
    """
    logger.info("Executing tool list_host_groups")
    return await _list(HostGroup, filters, limit, page, order)
