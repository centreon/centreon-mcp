from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.components.base import _delete, _list
from centreon_mcp.types.monitoring.downtime import (
    Downtime,
    DowntimeFilter,
    DowntimeOrder,
    DowntimeParams,
    DowntimeResource,
)
from centreon_mcp.utils import logger

downtime = FastMCP()


@downtime.tool(
    annotations={
        "title": "List hosts downtimes in real-time monitoring",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_downtimes(
    filters: list[DowntimeFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: DowntimeOrder | None = None,
) -> list[Downtime]:
    """
    List downtimes in real-time monitoring matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all downtimes except if explicitly intended.
    """
    logger.info("Executing tool list_downtimes")
    return await _list(Downtime, filters, limit, page, order)


@downtime.tool(
    annotations={
        "title": "Set a downtime on multiple resources (host and services) in real-time monitoring",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def set_downtimes(params: DowntimeParams, resources: list[DowntimeResource]) -> bool:
    """
    Add a downtime for multiple resources (host and services) in real-time monitoring.
    Use tool `list_resources` first to get resources IDs.
    """
    logger.info("Executing tool set_downtimes")
    return await Downtime.set(params, resources)


@downtime.tool(
    annotations={
        "title": "Cancel downtimes in real-time monitoring",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def cancel_downtimes(downtime_ids: list[int]) -> dict[int, bool | BaseException]:
    """
    Cancel multiple downtimes in real-time monitoring.
    Use tools `list_downtimes` first to get downtime IDs.
    """
    logger.info("Executing tool cancel_downtimes")
    return await _delete(Downtime, downtime_ids)
