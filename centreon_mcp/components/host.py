from typing import Annotated, ClassVar, List, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder, ConstraintLink, _list
from centreon_mcp.utils.type import (
    Host,
    HostGroup,
    HostState,
    MonitoringServer,
)

host = FastMCP()


class HostOrder(BaseOrder):
    field: Literal["host.name", "host.alias", "host.address", "host.state"] = (
        "host.name"
    )


class HostFilter(BaseFilter):
    links: ClassVar[list[ConstraintLink]] = [
        ConstraintLink(cls=HostGroup, object="host_group", fields=["name"]),
        ConstraintLink(cls=MonitoringServer, object="poller", fields=["name"]),
    ]

    # Fields available for filtering in Centreon API
    host_id: int | None = Field(None, serialization_alias="host.id")
    host_name: str | None = Field(None, serialization_alias="host.name")
    host_alias: str | None = Field(None, serialization_alias="host.alias")
    host_address: str | None = Field(None, serialization_alias="host.address")
    host_state: HostState | None = Field(None, serialization_alias="host.state")
    poller_id: int | None = Field(None, serialization_alias="poller.id")
    host_group_id: int | None = Field(None, serialization_alias="host_group.id")
    host_is_acknowledged: bool | None = Field(
        None, serialization_alias="host.is_acknowledged"
    )

    # Fields not available in Centreon API but useful for filtering
    host_group_name: str | None = Field(None, exclude=True)
    poller_name: str | None = Field(None, exclude=True)


@host.tool(
    annotations={
        "title": "List hosts in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_hosts(
    filters: List[HostFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 10,
    page: Annotated[int, Field(ge=1)] = 1,
    order: HostOrder | None = None,
) -> List[Host]:
    """
    List hosts in real-time monitoring matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all hosts except if explicitly intended.
    """
    return await _list(Host, HostOrder, filters, limit, page, order)
