from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.components.base import _create, _delete, _list
from centreon_mcp.types.host_category import (
    HostCategoryConfiguration,
    HostCategoryConfigurationFullParams,
    HostCategoryConfigurationPartialParams,
)
from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseFilter, BaseOrder

host_category = FastMCP()


class HostCategoryConfigurationOrder(BaseOrder):
    field: Literal["id", "name", "alias", "is_activated"] = "name"


class HostCategoryConfigurationFilter(BaseFilter):
    host_category_id: int | None = Field(None, serialization_alias="id $eq")
    host_category_name: str | None = Field(None, serialization_alias="name $eq")
    host_category_alias: str | None = Field(None, serialization_alias="alias $eq")
    host_category_is_activated: bool | None = Field(None, serialization_alias="is_activated $eq")


@host_category.tool(
    annotations={
        "title": "List host category configurations",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_host_category_configurations(
    filters: list[HostCategoryConfigurationFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: HostCategoryConfigurationOrder | None = None,
) -> list[HostCategoryConfiguration]:
    """
    List host category configurations matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all host categories except if explicitly intended.
    """
    logger.info("Executing tool list_host_category_configurations")
    return await _list(HostCategoryConfiguration, filters, limit, page, order)


@host_category.tool(
    annotations={
        "title": "Create a host category configuration",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def create_host_category_configuration(params: HostCategoryConfigurationFullParams) -> bool:
    """
    Create a host category configuration.
    """
    logger.info("Executing tool create_host_category_configuration")
    return await _create(HostCategoryConfiguration, params)


@host_category.tool(
    annotations={
        "title": "Update a host category configuration",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def update_host_category_configuration(
    host_category_id: int, params: HostCategoryConfigurationPartialParams
) -> bool:
    """
    Update a host category from params.
    """
    logger.info("Executing tool update_host_category_configuration")
    host_category = await HostCategoryConfiguration.get(host_category_id)
    data = host_category.model_dump(exclude={"id"}, exclude_none=True)
    data |= params.model_dump(exclude_none=True)
    return await HostCategoryConfiguration.update(
        host_category_id, HostCategoryConfigurationFullParams(**data)
    )


@host_category.tool(
    annotations={
        "title": "Delete host category configurations",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def delete_host_category_configurations(
    host_category_ids: list[int],
) -> dict[int, bool | BaseException]:
    """
    Delete multiple host category configurations.
    """
    logger.info("Executing tool delete_host_category_configurations")
    return await _delete(HostCategoryConfiguration, host_category_ids)
