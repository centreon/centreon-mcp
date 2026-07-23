from collections.abc import Sequence
from typing import Annotated, Literal, cast

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.types.monitoring import Monitoring, MonitoringFilter, MonitoringOrder
from centreon_mcp.types.monitoring.actions import (
    MonitoringAction,
    MonitoringActionFilter,
    MonitoringActionOrder,
    MonitoringActionParams,
)
from centreon_mcp.types.monitoring.mapping import MODELS_MIXIN_LIST, MODELS_MIXIN_SET
from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseResource

monitoring = FastMCP()


@monitoring.tool(
    annotations={
        "title": "List monitoring entities",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_monitoring_entities(
    model_type: Literal[
        "host_group",
        "service_group",
        "monitoring_server",
    ],
    filters: Sequence[MonitoringFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: MonitoringOrder | None = None,
) -> list[Monitoring]:
    """
    List real-time monitoring entities matching the given filters.
    The entities kind is selected via model_type:
        - Host Groups
        - Service Groups
        - Monitoring Servers
    If no filters are provided, ask users to provide at least one filter,
    unless retrieving all entities is explicitly intended.
    """
    logger.info("Executing tool list_monitoring")
    models = await MODELS_MIXIN_LIST[model_type].list(filters, limit, page, order)
    return cast(list[Monitoring], models)


@monitoring.tool(
    annotations={
        "title": "List monitoring actions",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_monitoring_actions(
    model_type: Literal["acknowledgement", "downtime"],
    filters: Sequence[MonitoringActionFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: MonitoringActionOrder | None = None,
) -> list[MonitoringAction]:
    """
    List real-time monitoring actions matching the given filters.
    The action kind is selected via model_type:
        - Acknowledgements
        - Downtimes
    If no filters are provided, ask users to provide at least one filter,
    unless retrieving all entities is explicitly intended.
    """
    logger.info("Executing tool list_monitoring_actions")
    models = await MODELS_MIXIN_LIST[model_type].list(filters, limit, page, order)
    return cast(list[MonitoringAction], models)


@monitoring.tool(
    annotations={
        "title": "Set monitoring actions",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def set_monitoring_actions(
    model_type: Literal["acknowledgement", "downtime", "comment", "check"],
    params: MonitoringActionParams,
    resources: list[BaseResource],
) -> bool:
    """
    Set a real-time monitoring actions on selected resources.
    The action kind is selected via model_type:
        - Acknowledgement
        - Downtime
        - Check
        - Comment
    """
    logger.info("Executing tool set_monitoring_actions")
    return await MODELS_MIXIN_SET[model_type].set(params, resources)
