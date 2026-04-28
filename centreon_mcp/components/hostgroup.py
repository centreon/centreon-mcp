from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseFilter, BaseOrder, _list
from centreon_mcp.utils.type import HostGroup, HostState

hostgroup = FastMCP()


class HostGroupOrder(BaseOrder):
    field: Literal["name", "host.name", "host.alias", "host.address", "host.state"] = "host.name"


class HostGroupFilter(BaseFilter):
    host_id: int | None = Field(None, serialization_alias="host.id $eq")
    host_name: str | None = Field(None, serialization_alias="host.name $eq")
    host_alias: str | None = Field(None, serialization_alias="host.alias $eq")
    host_address: str | None = Field(None, serialization_alias="host.address $eq")
    host_state: HostState | None = Field(None, serialization_alias="host.state $eq")
    poller_id: int | None = Field(None, serialization_alias="poller.id $eq")
    host_group_id: int | None = Field(None, serialization_alias="id $eq")
    host_group_name: str | None = Field(None, serialization_alias="name $eq")


@hostgroup.tool(
    annotations={
        "title": "List host groups in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_hostgroups(
    filters: list[HostGroupFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: HostGroupOrder | None = None,
) -> list[HostGroup]:
    """
    List host groups in real-time monitoring matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all host groups except if explicitly intended.
    """
    logger.info("Executing tool list_hostgroups")
    return await _list(HostGroup, HostGroupOrder, filters, limit, page, order)
