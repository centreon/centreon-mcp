import json
from typing import Annotated, List, Literal

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from centreon_mcp.utils.type import Host, HostState

host = FastMCP()


class HostOrder(BaseModel):
    field: Literal["host.name", "host.alias", "host.address", "host.state"] = (
        "host.name"
    )
    order: Literal["ASC", "DESC"] = "ASC"


class HostFilter(BaseModel):
    host_id: int | None = Field(None, serialization_alias="host.id")
    host_name: str | None = Field(None, serialization_alias="host.name")
    host_alias: str | None = Field(None, serialization_alias="host.alias")
    host_address: str | None = Field(None, serialization_alias="host.address")
    host_state: HostState | None = Field(None, serialization_alias="host.state")
    poller_id: int | None = Field(None, serialization_alias="poller.id")
    group_id: int | None = Field(None, serialization_alias="host_group.id")
    host_is_acknowledged: bool | None = Field(
        None, serialization_alias="host.is_acknowledged"
    )

    @property
    def conditions(self) -> List:
        """
        Generate list of conditions dictionary for filtering.
        """
        return [
            {name: {"$eq": value}}
            for name, value in self.model_dump(by_alias=True).items()
            if value is not None
        ]


@host.tool
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
    sort_by = json.dumps(order.model_dump())
    return await Host.list(search, limit, page, sort_by)
