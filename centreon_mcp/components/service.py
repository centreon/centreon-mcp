import json
from typing import Annotated, List, Literal

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter
from centreon_mcp.utils.type import Service, ServiceState

service = FastMCP()


class ServiceOrder(BaseModel):
    field: Literal[
        "host.name",
        "host.alias",
        "host.address",
        "host.state",
        "service.display_name",
        "service.description",
        "service.state",
    ] = "host.name"
    order: Literal["ASC", "DESC"] = "ASC"


class ServiceFilter(BaseFilter):
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
