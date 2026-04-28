import asyncio
from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseFilter, BaseOrder, _list
from centreon_mcp.utils.type import (
    Downtime,
    DowntimeParams,
    DowntimeResource,
    HostState,
)

downtime = FastMCP()


class DowntimeOrder(BaseOrder):
    field: Literal[
        "id",
        "host.id",
        "host.name",
        "host.alias",
        "host.address",
        "host.state",
        "start_time",
        "end_time",
        "entry_time",
        "deletion_time",
    ] = "id"


class DowntimeFilter(BaseFilter):
    host_id: int | None = Field(None, serialization_alias="host.id $eq")
    host_name: str | None = Field(None, serialization_alias="host.name $eq")
    host_alias: str | None = Field(None, serialization_alias="host.alias $eq")
    host_address: str | None = Field(None, serialization_alias="host.address $eq")
    host_state: HostState | None = Field(None, serialization_alias="host.state $eq")
    is_fixed: bool | None = Field(None, serialization_alias="is_fixed $eq")
    is_cancelled: bool | None = Field(None, serialization_alias="is_cancelled $eq")
    poller_id: int | None = Field(None, serialization_alias="poller.id $eq")


@downtime.tool(
    annotations={
        "title": "List hosts downtimes in real-time monitoring",
        "readOnlyHint": True,
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
    return await _list(Downtime, DowntimeOrder, filters, limit, page, order)


@downtime.tool(
    annotations={
        "title": "Set a downtime on multiple resources (host and services) in real-time monitoring",
        "readOnlyHint": False,
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
    await Downtime.set(params, resources)
    return True


@downtime.tool(
    annotations={
        "title": "Cancel downtimes in real-time monitoring",
        "readOnlyHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def cancel_downtimes(downtime_ids: list[int]) -> bool:
    """
    Cancel multiple downtimes in real-time monitoring.
    Use tools `list_downtimes` first to get downtime IDs.
    """
    logger.info("Executing tool cancel_downtimes")
    tasks = [asyncio.create_task(Downtime.cancel(downtime_id)) for downtime_id in downtime_ids]
    await asyncio.gather(*tasks)
    return True
