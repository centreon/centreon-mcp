from typing import Annotated, List, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder, _list
from centreon_mcp.utils.type import HostState, ServiceGroup

servicegroup = FastMCP()


class ServiceGroupOrder(BaseOrder):
    field: Literal[
        "name",
        "host.name",
        "host.alias",
        "host.address",
        "host.state",
        "service.name",
        "service.display_name",
    ] = "name"


class ServiceGroupFilter(BaseFilter):
    host_id: int | None = Field(None, serialization_alias="host.id")
    host_name: str | None = Field(None, serialization_alias="host.name")
    host_alias: str | None = Field(None, serialization_alias="host.alias")
    host_address: str | None = Field(None, serialization_alias="host.address")
    host_state: HostState | None = Field(None, serialization_alias="host.state")
    poller_id: int | None = Field(None, serialization_alias="poller.id")
    host_group_id: int | None = Field(None, serialization_alias="host_group.id")
    service_group_id: int | None = Field(None, serialization_alias="id")
    service_group_name: str | None = Field(None, serialization_alias="name")
    service_name: str | None = Field(None, serialization_alias="service.name")
    service_display_name: str | None = Field(
        None, serialization_alias="service.display_name"
    )
    host_group_name: str | None = Field(None, serialization_alias="host_group.name")


@servicegroup.tool(
    annotations={
        "title": "List service groups in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_servicegroups(
    filters: List[ServiceGroupFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 10,
    page: Annotated[int, Field(ge=1)] = 1,
    order: ServiceGroupOrder | None = None,
) -> List[ServiceGroup]:
    """
    List service groups in real-time monitoring matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all services groups except if explicitly intended.
    """
    return await _list(ServiceGroup, ServiceGroupOrder, filters, limit, page, order)
