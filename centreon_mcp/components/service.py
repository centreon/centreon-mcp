import json
from typing import List, Literal

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from centreon_mcp.type import HostState, Service

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


class ServiceFilter(BaseModel):
    host_id: int | None = Field(None, serialization_alias="host.id")
    host_name: str | None = Field(None, serialization_alias="host.name")
    host_alias: str | None = Field(None, serialization_alias="host.alias")
    host_address: str | None = Field(None, serialization_alias="host.address")
    host_state: HostState | None = Field(None, serialization_alias="host.state")
    host_group_id: int | None = Field(None, serialization_alias="host_group.id")
    service_display_name: str | None = Field(
        None, serialization_alias="service.display_name"
    )
    service_description: str | None = Field(
        None, serialization_alias="service.description"
    )
    service_state: int | None = Field(None, serialization_alias="service.state")
    service_group_id: int | None = Field(None, serialization_alias="service_group.id")
    poller_id: int | None = Field(None, serialization_alias="poller_id")

    @property
    def conditions(self) -> dict:
        """
        Generate conditions dictionary for filtering.
        """
        return {
            "$and": [
                {name: {"$eq": value}}
                for name, value in self.model_dump(by_alias=True).items()
                if value is not None
            ]
        }


@service.tool
async def list(
    filters: List[ServiceFilter] | None = None,
    limit: int = 20,
    page: int = 1,
    order: ServiceOrder | None = None,
) -> List[Service]:
    """
    List services matching the given filters.
    """
    filters = filters or []
    order = order or ServiceOrder()
    conditions = {"$or": [filter.conditions for filter in filters]}
    search = json.dumps(conditions)
    sort_by = json.dumps(order.model_dump())
    return await Service.list(search, limit, page, sort_by)
