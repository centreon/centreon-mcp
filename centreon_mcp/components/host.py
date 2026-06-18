import json
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.components.base import _create, _delete, _list, _patch
from centreon_mcp.types.configuration.host import (
    HostConfiguration,
    HostConfigurationFilter,
    HostConfigurationFullParams,
    HostConfigurationOrder,
    HostConfigurationPartialParams,
)
from centreon_mcp.types.monitoring.host import Host, HostFilter, HostStatusCount
from centreon_mcp.utils import logger

host = FastMCP()


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


@host.tool(
    annotations={
        "title": "List host configurations",
        "readOnlyHint": True,
        "destructiveHint": False,
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
    return await _list(HostConfiguration, filters, limit, page, order)


@host.tool(
    annotations={
        "title": "Create a host configuration",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def create_host_configuration(params: HostConfigurationFullParams) -> bool:
    """
    Create a host configuration from params.
    """
    logger.info("Executing tool create_host_configuration")
    return await _create(HostConfiguration, params)


@host.tool(
    annotations={
        "title": "Update a host configuration",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def update_host_configuration(host_id: int, params: HostConfigurationPartialParams) -> bool:
    """
    Update a host configuration from params.
    """
    logger.info("Executing tool update_host_configuration")
    return await _patch(HostConfiguration, host_id, params)


@host.tool(
    annotations={
        "title": "Delete host configurations",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def delete_host_configurations(host_ids: list[int]) -> dict[int, bool | BaseException]:
    """
    Delete multiple host configurations.
    """
    logger.info("Executing tool delete_host_configurations")
    return await _delete(HostConfiguration, host_ids)
