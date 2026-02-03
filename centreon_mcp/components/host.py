import asyncio
import json
from typing import Annotated, List, Literal

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder
from centreon_mcp.utils.type import Host, HostGroup, HostState

host = FastMCP()


class HostOrder(BaseOrder):
    field: Literal["host.name", "host.alias", "host.address", "host.state"] = (
        "host.name"
    )


class HostFilter(BaseFilter):
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

    async def complete(self) -> None:
        """
        Compute filters based on fields not available in Centreon API.
        """
        # Compute host_group_id if host_group_name is provided
        if self.host_group_name is not None:
            conditions = {"$and": [{"name": {"$eq": self.host_group_name}}]}
            hostgroups = await HostGroup.list(search=json.dumps(conditions))
            found = False
            for hostgroup in hostgroups:
                if hostgroup.name == self.host_group_name:
                    self.host_group_id, found = hostgroup.id, True
                    break
            if not found:
                raise ToolError(f"Host group '{self.host_group_name}' not found.")


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
    to avoid retrieving all hosts except if explicitly intended.
    """
    filters = filters or []
    order = order or HostOrder()
    await asyncio.gather(*(filter.complete() for filter in filters))
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
