from collections.abc import Sequence
from typing import Annotated, Literal, cast

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.types.configuration import (
    Configuration,
    ConfigurationFilter,
    ConfigurationFullParams,
    ConfigurationOrder,
    ConfigurationPartialParams,
)
from centreon_mcp.types.configuration.mapping import (
    MODELS_MIXIN_CREATE,
    MODELS_MIXIN_DELETE,
    MODELS_MIXIN_LIST,
    MODELS_MIXIN_UPDATE,
)
from centreon_mcp.utils import logger

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
    filters: Sequence[ConfigurationFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: ConfigurationOrder | None = None,
) -> list[Configuration]:
    """
    List configurations matching the given filters for following entities:
        - Commands
        - Hosts
        - Host Categories
        - Host Groups
        - Host Severities
        - Host Templates
        - Monitoring Servers
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all entities except if explicitly intended.
    """
    logger.info("Executing tool list_configurations")
    models = await MODELS_MIXIN_LIST[model_type].list(filters, limit, page, order)
    return [cast(Configuration, model) for model in models]


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
    Create a configuration for following entities:
        - Commands
        - Hosts
        - Host Categories
        - Host Groups
        - Host Severities
        - Host Templates
    """
    logger.info("Executing tool create_configuration")
    return await MODELS_MIXIN_CREATE[model_type].create(params)


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
    Update a configuration from partial params for following entities:
        - Hosts
        - Host Categories
        - Host Groups
        - Host Severities
        - Host Templates
    """
    logger.info("Executing tool update_configuration")
    return await MODELS_MIXIN_UPDATE[model_type].update(model_id, params)


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
    Delete multiple configurations from their ids for following entities:
        - Hosts
        - Host Categories
        - Host Groups
        - Host Severities
        - Host Templates
    """
    logger.info("Executing tool delete_configurations")
    return await MODELS_MIXIN_DELETE[model_type].delete(model_ids)
