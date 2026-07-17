from collections.abc import Sequence
from typing import Annotated, Literal, cast

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.types.monitoring import Monitoring, MonitoringFilter, MonitoringOrder
from centreon_mcp.types.monitoring.mapping import MODELS_MIXIN_LIST
from centreon_mcp.utils import logger

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
    return [cast(Monitoring, model) for model in models]
