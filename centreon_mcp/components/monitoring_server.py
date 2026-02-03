import json
from typing import Annotated, List, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder
from centreon_mcp.utils.type import MonitoringServer

monitoring_server = FastMCP()


class MonitoringServerOrder(BaseOrder):
    field: Literal["id", "name", "is_active", "is_localhost", "address"] = "name"


class MonitoringServerFilter(BaseFilter):
    monitoring_server_id: int | None = Field(None, serialization_alias="id")
    monitoring_server_name: str | None = Field(None, serialization_alias="name")
    monitoring_server_is_activate: bool | None = Field(
        None, serialization_alias="is_activate"
    )
    monitoring_server_is_localhost: bool | None = Field(
        None, serialization_alias="is_localhost"
    )
    monitoring_server_address: str | None = Field(None, serialization_alias="address")


@monitoring_server.tool(
    annotations={
        "title": "List monitoring servers configurations",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list(
    filters: List[MonitoringServerFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 10,
    page: Annotated[int, Field(ge=1)] = 1,
    order: MonitoringServerOrder | None = None,
) -> List[MonitoringServer]:
    """
    List monitoring servers configurations matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all monitoring servers except if explicitly intended.
    """
    order = order or MonitoringServerOrder()
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
    return await MonitoringServer.list(search, limit, page, sort_by)
