from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.components.base import _create, _delete, _list
from centreon_mcp.types.host import HostState
from centreon_mcp.types.host_group import (
    HostGroup,
    HostGroupConfiguration,
    HostGroupConfigurationFullParams,
    HostGroupConfigurationPartialParams,
)
from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseFilter, BaseOrder

host_group = FastMCP()


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


class HostGroupConfigurationOrder(BaseOrder):
    field: Literal["id", "name", "alias", "is_activated"] = "name"


class HostGroupConfigurationFilter(BaseFilter):
    host_group_id: int | None = Field(None, serialization_alias="id $eq")
    host_group_name: str | None = Field(None, serialization_alias="name $eq")
    host_group_alias: str | None = Field(None, serialization_alias="alias $eq")
    host_group_is_activated: bool | None = Field(None, serialization_alias="is_activated $eq")


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
    Update a host group from params.
    """
    logger.info("Executing tool update_host_group_configuration")
    hostgroup = await HostGroupConfiguration.get(host_group_id)
    data = hostgroup.model_dump(exclude={"id", "is_activated", "icon", "hosts"}, exclude_none=True)
    data["icon_id"] = hostgroup.icon.id if hostgroup.icon else None
    data["hosts"] = [host.id for host in hostgroup.hosts if host.id not in params.hosts_removed]
    data["hosts"] += [host_id for host_id in params.hosts_added if host_id not in data["hosts"]]
    data |= params.model_dump(exclude_none=True)
    return await HostGroupConfiguration.update(
        host_group_id, HostGroupConfigurationFullParams(**data)
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
