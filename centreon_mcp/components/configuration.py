from collections.abc import Sequence
from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.components.base import _create, _delete, _list, _patch, _update
from centreon_mcp.types import (
    MODELS_MIXIN_CREATE,
    MODELS_MIXIN_DELETE,
    MODELS_MIXIN_LIST,
    MODELS_MIXIN_PATCH,
    MODELS_MIXIN_UPDATE,
)
from centreon_mcp.types.configuration import (
    CONFIGURATIONS_FULL_PARAMS,
    ConfigurationFilter,
    ConfigurationFullParams,
    ConfigurationOrder,
    ConfigurationPartialParams,
)
from centreon_mcp.utils import logger
from centreon_mcp.utils.mixins import ListMixin

configuration = FastMCP()


@configuration.tool(
    annotations={
        "title": "List configurations",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_configurations(
    model_type: Literal[
        "command",
        "host_category",
        "host_group",
        "host_severity",
        "host_template",
        "host",
        "monitoring_server",
    ],
    filters: list[ConfigurationFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: ConfigurationOrder | None = None,
) -> Sequence[ListMixin]:
    """
    List configurations matching the given filters for follwoing entities:
        - Commands
        - Hosts
        - Host Categories
        - Host Groups
        - Hosts Severities
        - Host Templates
        - Monitoring Servers
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all commands except if explicitly intended.
    """
    logger.info("Executing tool list_configurations")
    return await _list(MODELS_MIXIN_LIST[model_type], filters, limit, page, order)


@configuration.tool(
    annotations={
        "title": "Create a configuration",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def create_configuration(
    model_type: Literal[
        "command", "host_category", "host_group", "host_severity", "host_template", "host"
    ],
    params: ConfigurationFullParams,
) -> bool:
    """
    Create a configuration for follwoing entities:
        - Commands
        - Hosts
        - Host Categories
        - Host Groups
        - Hosts Severities
        - Host Templates
    """
    logger.info("Executing tool create_configuration")
    return await _create(MODELS_MIXIN_CREATE[model_type], params)


@configuration.tool(
    annotations={
        "title": "Update a configuration",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def update_configuration(
    model_type: Literal["host_category", "host_group", "host_severity", "host_template", "host"],
    model_id: int,
    params: ConfigurationPartialParams,
) -> bool:
    """
    Update a configuration from partial params for follwoing entities:
        - Hosts
        - Host Categories
        - Host Groups
        - Hosts Severities
        - Host Templates
    """
    logger.info("Executing tool update_configuration")

    if model_type in ["host", "host_template"]:
        return await _patch(MODELS_MIXIN_PATCH[model_type], model_id, params)

    else:
        return await _update(
            MODELS_MIXIN_UPDATE[model_type],
            CONFIGURATIONS_FULL_PARAMS[model_type],
            model_id,
            params,
        )


@configuration.tool(
    annotations={
        "title": "Delete configurations",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def delete_configurations(
    model_type: Literal["host_category", "host_group", "host_severity", "host_template", "host"],
    model_ids: list[int],
) -> dict[int, bool | BaseException]:
    """
    Delete multiple configurations from their ids for follwoing entities:
        - Hosts
        - Host Categories
        - Host Groups
        - Hosts Severities
        - Host Templates
    """
    logger.info("Executing tool delete_configurations")
    return await _delete(MODELS_MIXIN_DELETE[model_type], model_ids)
