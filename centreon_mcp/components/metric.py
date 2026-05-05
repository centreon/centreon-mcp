from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils import logger
from centreon_mcp.utils.type import Metric

metric = FastMCP()


@metric.tool(
    annotations={
        "title": "Get metrics of a service",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def get_service_metrics(
    host_id: Annotated[int, Field(ge=1, description="ID of the host")],
    service_id: Annotated[int, Field(ge=1, description="ID of the service")],
) -> list[Metric]:
    """
    Get all metrics of a service with their current values and thresholds.
    Returns metric name, unit, current value, and warning/critical thresholds.
    Use list_resources first to obtain the host_id and service_id.
    """
    logger.info("Executing tool get_service_metrics")
    return await Metric.list(host_id, service_id)
