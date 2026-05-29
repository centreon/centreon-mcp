import asyncio
from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.types.host_template import (
    HostTemplate,
    HostTemplateFullParams,
    HostTemplatePartialParams,
)
from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseFilter, BaseOrder, _list

host_template = FastMCP()


class HostTemplateOrder(BaseOrder):
    field: Literal["name", "alias"] = "name"


class HostTemplateFilter(BaseFilter):
    host_template_id: int | None = Field(None, serialization_alias="id $eq")
    host_template_name: str | None = Field(None, serialization_alias="name $eq")
    host_template_alias: str | None = Field(None, serialization_alias="alias $eq")
    is_locked: bool | None = Field(None, serialization_alias="is_locked $eq")


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
    return await _list(HostTemplate, HostTemplateOrder, filters, limit, page, order)


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
    return await HostTemplate.create(params)


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
    return await HostTemplate.patch(host_template_id, params)


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
    tasks = [
        asyncio.create_task(HostTemplate.delete(host_template_id))
        for host_template_id in host_template_ids
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return dict(zip(host_template_ids, results, strict=True))
