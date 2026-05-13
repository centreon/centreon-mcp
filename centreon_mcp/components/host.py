import asyncio
import json
from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.types.host import (
    Host,
    HostConfiguration,
    HostConfigurationParams,
    HostStatusCount,
)
from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseFilter, BaseOrder, _list

host = FastMCP()


class HostFilter(BaseFilter):
    host_group_id: int | None = Field(None, serialization_alias="host_group.id $eq")
    host_group_name: str | None = Field(None, serialization_alias="host_group.name $eq")
    host_category_id: int | None = Field(None, serialization_alias="host_category.id $eq")
    host_category_name: str | None = Field(None, serialization_alias="host_category.name $eq")


@host.tool(
    annotations={
        "title": "Count hosts by status in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def count_hosts_by_status(
    filters: list[HostFilter] | None = None,
) -> HostStatusCount:
    """
    Count hosts by status in real-time monitoring.
    Returns the total number of hosts in each state: UP, DOWN, UNREACHABLE, and PENDING.
    Each filter object narrows results by host group or host category.
    Fields within a single filter are ANDed together, multiple filter objects are ORed.
    Omit filters to count all hosts.
    Use this tool instead of list_resources when only aggregate counts are needed
    """
    logger.info("Executing tool count_hosts_by_status")
    search = json.dumps(HostFilter.join(filters))
    return await Host.count_by_status(search)


class HostConfigurationOrder(BaseOrder):
    field: Literal["name", "alias", "address"] = "name"


class HostConfigurationFilter(BaseFilter):
    host_configuration_id: int | None = Field(None, serialization_alias="id $eq")
    host_configuration_name: str | None = Field(None, serialization_alias="name $eq")
    host_configuration_address: str | None = Field(None, serialization_alias="address $eq")
    poller_id: int | None = Field(None, serialization_alias="poller.id $eq")
    poller_name: str | None = Field(None, serialization_alias="poller.name $eq")
    host_group_id: int | None = Field(None, serialization_alias="group.id $eq")
    host_group_name: str | None = Field(None, serialization_alias="group.name $eq")
    host_category_id: int | None = Field(None, serialization_alias="category.id $eq")
    host_category_name: str | None = Field(None, serialization_alias="category.name $eq")
    is_activated: bool | None = Field(None, serialization_alias="is_activated $eq")


@host.tool(
    annotations={
        "title": "List host configurations",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_host_configurations(
    filters: list[HostConfigurationFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: HostConfigurationOrder | None = None,
) -> list[HostConfiguration]:
    """
    List host configurations matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all host configurations except if explicitly intended.
    """
    logger.info("Executing tool list_host_configurations")
    return await _list(HostConfiguration, HostConfigurationOrder, filters, limit, page, order)


@host.tool(
    annotations={
        "title": "Create a host configuration",
        "readOnlyHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def create_host_configuration(params: HostConfigurationParams) -> bool:
    """
    Create a host configuration from params.
    """
    logger.info("Executing tool create_host_configuration")
    return await HostConfiguration.create(params)


@host.tool(
    annotations={
        "title": "Update a host configuration",
        "readOnlyHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def update_host_configuration(host_id: int, params: HostConfigurationParams) -> bool:
    """
    Update a host configuration from params.
    """
    logger.info("Executing tool update_host_configuration")
    return await HostConfiguration.update(host_id, params)


@host.tool(
    annotations={
        "title": "Delete host configurations",
        "readOnlyHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def delete_host_configurations(host_ids: list[int]) -> dict[int, bool | BaseException]:
    """
    Delete multiple host configurations.
    """
    logger.info("Executing tool delete_host_configurations")
    tasks = [asyncio.create_task(HostConfiguration.delete(host_id)) for host_id in host_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return dict(zip(host_ids, results, strict=True))
