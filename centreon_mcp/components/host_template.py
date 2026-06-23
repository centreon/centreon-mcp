from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.components.base import _create, _delete, _list, _patch
from centreon_mcp.types.configuration.host_template import (
    HostTemplate,
    HostTemplateFilter,
    HostTemplateFullParams,
    HostTemplateOrder,
    HostTemplatePartialParams,
)
from centreon_mcp.utils import logger

host_template = FastMCP()


@host_template.tool(
    annotations={
        "title": "List host templates",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_host_templates(
    filters: list[HostTemplateFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: HostTemplateOrder | None = None,
) -> list[HostTemplate]:
    """
    List host templates matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all host templates except if explicitly intended.
    """
    logger.info("Executing tool list_host_templates")
    return await _list(HostTemplate, filters, limit, page, order)


@host_template.tool(
    annotations={
        "title": "Create a host template",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def create_host_template(params: HostTemplateFullParams) -> bool:
    """
    Create a host template from params.
    """
    logger.info("Executing tool create_host_template")
    return await _create(HostTemplate, params)


@host_template.tool(
    annotations={
        "title": "Update a host template",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def update_host_template(host_template_id: int, params: HostTemplatePartialParams) -> bool:
    """
    Update a host template from params.
    """
    logger.info("Executing tool update_host_template")
    return await _patch(HostTemplate, host_template_id, params)


@host_template.tool(
    annotations={
        "title": "Delete host templates",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def delete_host_templates(host_template_ids: list[int]) -> dict[int, bool | BaseException]:
    """
    Delete multiple host templates.
    """
    logger.info("Executing tool delete_host_templates")
    return await _delete(HostTemplate, host_template_ids)
