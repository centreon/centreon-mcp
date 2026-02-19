import asyncio
import json
from typing import Annotated, ClassVar, List, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder, ConstraintLink
from centreon_mcp.utils.type import (
    HostDowntime,
    HostState,
    MonitoringServer,
    ServiceDowntime,
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
    links: ClassVar[list[ConstraintLink]] = [
        ConstraintLink(cls=MonitoringServer, object="poller", fields=["name"]),
    ]

    # Fields available for filtering in Centreon API
    host_id: int | None = Field(None, serialization_alias="host.id")
    host_name: str | None = Field(None, serialization_alias="host.name")
    host_alias: str | None = Field(None, serialization_alias="host.alias")
    host_address: str | None = Field(None, serialization_alias="host.address")
    host_state: HostState | None = Field(None, serialization_alias="host.state")
    is_fixed: bool | None = Field(None, serialization_alias="is_fixed")
    is_cancelled: bool | None = Field(None, serialization_alias="is_cancelled")
    poller_id: int | None = Field(None, serialization_alias="poller.id")

    # Fields not available in Centreon API but useful for filtering
    poller_name: str | None = Field(None, exclude=True)


@downtime.tool(
    annotations={
        "title": "List hosts downtimes in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_host(
    filters: List[DowntimeFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 10,
    page: Annotated[int, Field(ge=1)] = 1,
    order: DowntimeOrder | None = None,
) -> List[HostDowntime]:
    """
    List host downtimes in real-time monitoring matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all host downtimes except if explicitly intended.
    """
    filters = filters or []
    order = order or DowntimeOrder()
    await asyncio.gather(*(filter.complete() for filter in filters))
    conditions = (
        {
            "$or": [
                {"$and": filter.conditions} for filter in filters if filter.conditions
            ]
        }
        if filters
        else {}
    )
    search = json.dumps(conditions)
    sort_by = order.model_dump_json()
    return await HostDowntime.list(search, limit, page, sort_by)


@downtime.tool(
    annotations={
        "title": "List service downtimes in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_service(
    filters: List[DowntimeFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 10,
    page: Annotated[int, Field(ge=1)] = 1,
    order: DowntimeOrder | None = None,
) -> List[ServiceDowntime]:
    """
    List service downtimes in real-time monitoring matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all service downtimes except if explicitly intended.
    """
    filters = filters or []
    order = order or DowntimeOrder()
    await asyncio.gather(*(filter.complete() for filter in filters))
    conditions = (
        {
            "$or": [
                {"$and": filter.conditions} for filter in filters if filter.conditions
            ]
        }
        if filters
        else {}
    )
    search = json.dumps(conditions)
    sort_by = order.model_dump_json()
    return await ServiceDowntime.list(search, limit, page, sort_by)
