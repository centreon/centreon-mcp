import json
from typing import Annotated, List, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder
from centreon_mcp.utils.type import Host

host = FastMCP()


class HostOrder(BaseOrder):
    field: Literal["host.name", "host.alias", "host.address", "host.state"] = (
        "host.name"
    )


class HostFilter(BaseFilter):
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
