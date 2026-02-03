import json
from typing import Annotated, List, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder
from centreon_mcp.utils.type import HostState, Service, ServiceState

service = FastMCP()


class ServiceOrder(BaseOrder):
    field: Literal[
        "host.name",
        "host.alias",
        "host.address",
        "host.state",
        "service.display_name",
        "service.description",
        "service.state",
    ] = "host.name"


class ServiceFilter(BaseFilter):
    host_id: int | None = Field(None, serialization_alias="host.id")
    host_name: str | None = Field(None, serialization_alias="host.name")
    host_alias: str | None = Field(None, serialization_alias="host.alias")
    host_address: str | None = Field(None, serialization_alias="host.address")
    host_state: HostState | None = Field(None, serialization_alias="host.state")
    poller_id: int | None = Field(None, serialization_alias="poller.id")
    host_group_id: int | None = Field(None, serialization_alias="host_group.id")
    service_display_name: str | None = Field(
        None, serialization_alias="service.display_name"
    )
    service_description: str | None = Field(
        None, serialization_alias="service.description"
    )
    service_state: ServiceState | None = Field(
        None, serialization_alias="service.state"
    )
    service_group_id: int | None = Field(None, serialization_alias="service_group.id")


@service.tool(
    annotations={
        "title": "List services in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list(
    filters: List[ServiceFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 10,
    page: Annotated[int, Field(ge=1)] = 1,
    order: ServiceOrder | None = None,
) -> List[Service]:
    """
    List services in real-time monitoring matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all services except if explicitly intended.
    """
    order = order or ServiceOrder()
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
    return await Service.list(search, limit, page, sort_by)
