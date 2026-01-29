import json
from typing import Annotated, List, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder
from centreon_mcp.utils.type import HostGroup

hostgroup = FastMCP()


class HostGroupOrder(BaseOrder):
    field: Literal["name", "host.name", "host.alias", "host.address", "host.state"] = (
        "host.name"
    )


class HostGroupFilter(BaseFilter):
    host_group_id: int | None = Field(None, serialization_alias="id")
    host_group_name: str | None = Field(None, serialization_alias="name")


@hostgroup.tool(
    annotations={
        "title": "List host groups in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list(
    filters: List[HostGroupFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 10,
    page: Annotated[int, Field(ge=1)] = 1,
    order: HostGroupOrder | None = None,
) -> List[HostGroup]:
    """
    List host groups in real-time monitoring matching the given filters.
    """
    order = order or HostGroupOrder()
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
    return await HostGroup.list(search, limit, page, sort_by)
