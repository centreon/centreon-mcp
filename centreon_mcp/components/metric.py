from fastmcp import FastMCP

from centreon_mcp.types.monitoring.metric import Metric
from centreon_mcp.utils import logger

metric = FastMCP()


@metric.tool(
    annotations={
        "title": "Get metrics of a service",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def get_service_metrics(host_id: int, service_id: int) -> list[Metric]:
    """
    Get all metrics of a service with their current values and thresholds.
    Returns metric name, unit, current value, and warning/critical thresholds.
    Use list_monitoring_resources first to obtain the host_id and service_id.
    """
    logger.info("Executing tool get_service_metrics")
    return await Metric.list(host_id, service_id)
