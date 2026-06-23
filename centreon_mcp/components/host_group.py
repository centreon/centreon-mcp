from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.components.base import _create, _delete, _list, _update
from centreon_mcp.types.configuration.host_group import (
    HostGroupConfiguration,
    HostGroupConfigurationFilter,
    HostGroupConfigurationFullParams,
    HostGroupConfigurationOrder,
    HostGroupConfigurationPartialParams,
)
from centreon_mcp.types.monitoring.host_group import HostGroup, HostGroupFilter, HostGroupOrder
from centreon_mcp.utils import logger

host_group = FastMCP()


@host_group.tool(
    annotations={
        "title": "List host groups in real-time monitoring",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_host_groups(
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
    logger.info("Executing tool list_host_groups")
    return await _list(HostGroup, filters, limit, page, order)


@host_group.tool(
    annotations={
        "title": "List host groups configurations",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_host_group_configurations(
    filters: list[HostGroupConfigurationFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: HostGroupConfigurationOrder | None = None,
) -> list[HostGroupConfiguration]:
    """
    List host groups configurations matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all host groups except if explicitly intended.
    """
    logger.info("Executing tool list_hostgroup_configurations")
    return await _list(HostGroupConfiguration, filters, limit, page, order)


@host_group.tool(
    annotations={
        "title": "Add a host group configuration",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def create_host_group_configuration(params: HostGroupConfigurationFullParams) -> bool:
    """
    Create a hostgroup.
    """
    logger.info("Executing tool create_hostgroup_configuration")
    return await _create(HostGroupConfiguration, params)


@host_group.tool(
    annotations={
        "title": "Update a host group configuration",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def update_host_group_configuration(
    host_group_id: int, params: HostGroupConfigurationPartialParams
) -> bool:
    """
    Update a host group from params. Just need to get host_group_id first.
    """
    logger.info("Executing tool update_host_group_configuration")
    return await _update(
        HostGroupConfiguration, HostGroupConfigurationFullParams, host_group_id, params
    )


@host_group.tool(
    annotations={
        "title": "Delete host group configurations",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def delete_host_group_configurations(
    hostgroup_ids: list[int],
) -> dict[int, bool | BaseException]:
    """
    Delete multiple host group configurations.
    """
    logger.info("Executing tool delete_host_group_configurations")
    return await _delete(HostGroupConfiguration, hostgroup_ids)
