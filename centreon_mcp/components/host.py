import json
from typing import Annotated, List, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder
from centreon_mcp.utils.type import Host, HostState

host = FastMCP()


class HostOrder(BaseOrder):
    field: Literal["host.name", "host.alias", "host.address", "host.state"] = (
        "host.name"
    )


class HostFilter(BaseFilter):
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


@host.tool(
    annotations={
        "title": "List hosts in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list(
    filters: List[HostFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 10,
    page: Annotated[int, Field(ge=1)] = 1,
    order: HostOrder | None = None,
) -> List[Host]:
    """
    List hosts in real-time monitoring matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all hosts  except if explicitly intended.
    """
    order = order or HostOrder()
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
    return await Host.list(search, limit, page, sort_by)
