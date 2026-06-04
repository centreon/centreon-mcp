from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.components.base import _create, _delete, _list, _update
from centreon_mcp.types.host_severity import (
    HostSeverity,
    HostSeverityFullParams,
    HostSeverityPartialParams,
)
from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseFilter, BaseOrder

host_severity = FastMCP()


class HostSeverityOrder(BaseOrder):
    field: Literal["name", "alias", "level"] = "name"


class HostSeverityFilter(BaseFilter):
    host_severity_id: int | None = Field(None, serialization_alias="id $eq")
    host_severity_name: str | None = Field(None, serialization_alias="name $eq")
    host_severity_alias: str | None = Field(None, serialization_alias="alias $eq")
    min_host_severity_level: int | None = Field(None, serialization_alias="level $ge")
    max_host_severity_level: int | None = Field(None, serialization_alias="level $le")
    host_severity_is_activated: bool | None = Field(None, serialization_alias="is_activated $eq")


@host_severity.tool(
    annotations={
        "title": "List host severities",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_host_severities(
    filters: list[HostSeverityFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: HostSeverityOrder | None = None,
) -> list[HostSeverity]:
    """
    List host severities matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all host severities except if explicitly intended.
    """
    logger.info("Executing tool list_host_severities")
    return await _list(HostSeverity, filters, limit, page, order)


@host_severity.tool(
    annotations={
        "title": "Create a host severity",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def create_host_severity(params: HostSeverityFullParams) -> bool:
    """
    Create a host severity from params.
    """
    logger.info("Executing tool create_host_severity")
    return await _create(HostSeverity, params)


@host_severity.tool(
    annotations={
        "title": "Update a host severity",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def update_host_severity(host_severity_id: int, params: HostSeverityPartialParams) -> bool:
    """
    Update a host severity from params.
    """
    logger.info("Executing tool update_host_severity")
    return await _update(HostSeverity, HostSeverityFullParams, host_severity_id, params)


@host_severity.tool(
    annotations={
        "title": "Delete host severities",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def delete_host_severities(host_severity_ids: list[int]) -> dict[int, bool | BaseException]:
    """
    Delete multiple host severities.
    Use tools `list_host_severities` first to get host severities IDs.
    """
    logger.info("Executing tool delete_host_severities")
    return await _delete(HostSeverity, host_severity_ids)
