import json
from typing import Annotated, List, Literal

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from centreon_mcp.utils.type import HostState, Service, ServiceState

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
    service_state: ServiceState | None = Field(
        None, serialization_alias="service.state"
    )
    service_group_id: int | None = Field(None, serialization_alias="service_group.id")
    poller_id: int | None = Field(None, serialization_alias="poller_id")

    @property
    def conditions(self) -> List[dict]:
        """
        Generate list of conditions dictionary for filtering.
        """
        return [
            {name: {"$eq": value}}
            for name, value in self.model_dump(by_alias=True).items()
            if value is not None
        ]


@service.tool
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
    sort_by = json.dumps(order.model_dump())
    return await Service.list(search, limit, page, sort_by)
