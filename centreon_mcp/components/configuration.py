import asyncio
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
from centreon_mcp.types.configuration.monitoring_server import MonitoringServer
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
        "host",
        "host_category",
        "host_group",
        "host_severity",
        "host_template",
        "monitoring_server",
        "service",
        "service_category",
        "service_group",
        "service_severity",
        "service_template",
        "time_period",
    ],
    filters: Sequence[ConfigurationFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: ConfigurationOrder | None = None,
) -> list[Configuration]:
    """
    List configurations matching the given filters for following entities:
        - Host / Service
        - Host / Service Category
        - Host / Service Group
        - Host / Service Severity
        - Host / Service Template
        - Commands
        - Monitoring Servers
        - Time Periods
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all entities except if explicitly intended.
    """
    logger.info("Executing tool list_configurations")

    # Check compatibility between model and order types
    if order is not None:
        order.check(model_type)

    # Check compatibility between model and filters types
    if filters is not None:
        [f.check(model_type) for f in filters]

    models = await MODELS_MIXIN_LIST[model_type].list(filters, limit, page, order)
    return cast(list[Configuration], models)


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
        "command",
        "host",
        "host_category",
        "host_group",
        "host_severity",
        "host_template",
        "service",
        "service_category",
        "service_group",
        "service_severity",
        "service_template",
        "time_period",
    ],
    params: ConfigurationFullParams,
) -> bool:
    """
    Create a configuration for following entities:
        - Host / Service
        - Host / Service Category
        - Host / Service Group
        - Host / Service Severity
        - Host / Service Template
        - Commands
        - Time Periods
    """
    logger.info("Executing tool create_configuration")

    # Check compatibility between model and params types
    params.check(model_type)

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
    model_type: Literal[
        "host",
        "host_category",
        "host_group",
        "host_severity",
        "host_template",
        "service",
        "service_severity",
        "service_template",
        "time_period",
    ],
    model_id: int,
    params: ConfigurationPartialParams,
) -> bool:
    """
    Update a configuration from partial params for following entities:
        - Host / Service
        - Host Category
        - Host Group
        - Host / Service Severity
        - Host / Service Template
        - Time Periods
    """
    logger.info("Executing tool update_configuration")

    # Check compatibility between model and params types
    params.check(model_type)

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
    model_type: Literal[
        "host",
        "host_category",
        "host_group",
        "host_severity",
        "host_template",
        "service",
        "service_category",
        "service_group",
        "service_severity",
        "service_template",
        "time_period",
    ],
    model_ids: list[int],
) -> dict[int, bool | BaseException]:
    """
    Delete multiple configurations from their ids for following entities:
        - Host / Service
        - Host / Service Category
        - Host / Service Group
        - Host / Service Severity
        - Host / Service Template
        - Time Periods
    """
    logger.info("Executing tool delete_configurations")
    return await MODELS_MIXIN_DELETE[model_type].delete(model_ids)


@configuration.tool(
    annotations={
        "title": "Generate/Reload monitoring server configurations",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def manage_monitoring_server_configurations(
    action: Literal["generate", "reload"],
    monitoring_server_ids: list[int] | None = None,
) -> bool | dict[int, bool | BaseException]:
    """
    Generate/Reload configurations of monitoring servers based on their ids.
    If no ids provided, generate/reload configurations of all monitoring servers.
    """
    logger.info("Executing tool manage_monitoring_server_configurations")

    # If no ids, generate/reload all configurations
    if monitoring_server_ids is None:
        return await MonitoringServer.manage(action)

    # Else, generate/reload configurations concurrently
    tasks = [
        asyncio.create_task(MonitoringServer.manage(action, monitoring_server_id))
        for monitoring_server_id in monitoring_server_ids
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return dict(zip(monitoring_server_ids, results, strict=True))
