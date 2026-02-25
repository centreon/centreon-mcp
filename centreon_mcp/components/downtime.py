from datetime import datetime
from typing import Annotated, ClassVar, Literal

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder, ConstraintLink, _list
from centreon_mcp.utils.type import (
    BaseDowntime,
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
    host_id: int | None = Field(None, serialization_alias="host.id $eq")
    host_name: str | None = Field(None, serialization_alias="host.name $eq")
    host_alias: str | None = Field(None, serialization_alias="host.alias $eq")
    host_address: str | None = Field(None, serialization_alias="host.address $eq")
    host_state: HostState | None = Field(None, serialization_alias="host.state $eq")
    is_fixed: bool | None = Field(None, serialization_alias="is_fixed $eq")
    is_cancelled: bool | None = Field(None, serialization_alias="is_cancelled $eq")
    poller_id: int | None = Field(None, serialization_alias="poller.id $eq")

    # Fields not available in Centreon API but useful for filtering
    poller_name: str | None = Field(None, exclude=True)


class DowntimeParams(BaseModel):
    start_time: datetime
    end_time: datetime
    is_fixed: bool
    duration: int
    comment: str


class HostDowntimeParams(DowntimeParams):
    with_services: bool


class ServiceDowntimeParams(DowntimeParams):
    pass


@downtime.tool(
    annotations={
        "title": "List hosts downtimes in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_host_downtimes(
    filters: list[DowntimeFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 10,
    page: Annotated[int, Field(ge=1)] = 1,
    order: DowntimeOrder | None = None,
) -> list[HostDowntime]:
    """
    List host downtimes in real-time monitoring matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all host downtimes except if explicitly intended.
    """
    return await _list(HostDowntime, DowntimeOrder, filters, limit, page, order)


@downtime.tool(
    annotations={
        "title": "List service downtimes in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_service_downtimes(
    filters: list[DowntimeFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 10,
    page: Annotated[int, Field(ge=1)] = 1,
    order: DowntimeOrder | None = None,
) -> list[ServiceDowntime]:
    """
    List service downtimes in real-time monitoring matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all service downtimes except if explicitly intended.
    """
    return await _list(ServiceDowntime, DowntimeOrder, filters, limit, page, order)


@downtime.tool(
    annotations={
        "title": "Add host downtimes in real-time monitoring",
        "readOnlyHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def add_host_downtimes(
    host_ids: list[int], downtimes: list[HostDowntimeParams]
) -> bool:
    """
    Add each downtime for each host in real-time monitoring.
    Use tool `list_resources` with type 'host' first to get host IDs.
    """
    payload = [
        {"resource_id": host_id, **downtime.model_dump(mode="json")}
        for host_id in host_ids
        for downtime in downtimes
    ]
    await HostDowntime.add(payload)
    return True


@downtime.tool(
    annotations={
        "title": "Add service downtimes in real-time monitoring",
        "readOnlyHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def add_service_downtimes(
    host_id: int,
    service_ids: list[int],
    downtimes: list[ServiceDowntimeParams],
) -> bool:
    """
    Add each downtime for each service of a given host in real-time monitoring.
    Use tool `list_resources` with type 'service' first to get service IDs.
    """
    payload = [
        {
            "resource_id": service_id,
            "parent_resource_id": host_id,
            **downtime.model_dump(mode="json"),
        }
        for service_id in service_ids
        for downtime in downtimes
    ]
    await ServiceDowntime.add(payload)
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
    Use tools `list_host_downtimes` and/or `list_service_downtimes` first to get downtime IDs.
    """
    await BaseDowntime.cancel(downtime_ids)
    return True
