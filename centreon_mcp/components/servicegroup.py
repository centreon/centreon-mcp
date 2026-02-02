import json
from typing import Annotated, List, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder
from centreon_mcp.utils.type import ServiceGroup

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
async def list(
    filters: List[ServiceGroupFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 10,
    page: Annotated[int, Field(ge=1)] = 1,
    order: ServiceGroupOrder | None = None,
) -> List[ServiceGroup]:
    """
    List service groups in real-time monitoring matching the given filters.
    """
    order = order or ServiceGroupOrder()
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
    return await ServiceGroup.list(search, limit, page, sort_by)
