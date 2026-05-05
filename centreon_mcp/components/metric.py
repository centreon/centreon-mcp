from datetime import datetime
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils import logger
from centreon_mcp.utils.type import Metric, PerformanceData, TopMetricResult

metric = FastMCP()


@metric.tool(
    annotations={
        "title": "Get current metric values and thresholds for a service",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def get_service_metrics(host_id: int, service_id: int) -> list[Metric]:
    """
    Get all metrics of a service with their current values, units, and warning/critical thresholds.
    Useful to answer "what is the current CPU usage?" or "how close is disk usage to the critical threshold?"
    Use tool `list_resources` first to get the host_id and service_id.
    """
    logger.info("Executing tool get_service_metrics")
    return await Metric.list(host_id, service_id)


@metric.tool(
    annotations={
        "title": "Get historical performance data (time series) for a service",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def get_metric_performance_data(
    host_id: int,
    service_id: int,
    start: Annotated[
        str | None,
        Field(
            description=(
                "Start of the time range in ISO8601 format (e.g. 2024-01-15T08:00:00Z). "
                "Defaults to 24 hours ago if omitted."
            ),
        ),
    ] = None,
    end: Annotated[
        str | None,
        Field(
            description=(
                "End of the time range in ISO8601 format (e.g. 2024-01-15T20:00:00Z). "
                "Defaults to now if omitted."
            ),
        ),
    ] = None,
) -> PerformanceData:
    """
    Get historical performance data (time series) for all metrics of a service.
    Returns timestamped data points for each metric, enabling trend analysis.
    Useful to answer "how has CPU evolved over the last 6 hours?" or "when did disk usage start increasing?"
    Use tool `list_resources` first to get the host_id and service_id.
    """
    logger.info("Executing tool get_metric_performance_data")
    if start is not None:
        datetime.fromisoformat(start)
    if end is not None:
        datetime.fromisoformat(end)
    return await PerformanceData.get(host_id, service_id, start, end)


@metric.tool(
    annotations={
        "title": "Get top/bottom resources ranked by a given metric",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def get_top_resources_by_metric(
    metric_name: Annotated[
        str,
        Field(
            description=(
                "Name of the metric to rank by (e.g. 'cpu', 'used', 'rta', 'pl'). "
                "Must match the exact metric name as returned by get_service_metrics."
            ),
            min_length=1,
            max_length=255,
        ),
    ],
) -> TopMetricResult:
    """
    Get the top resources (hosts/services) ranked by current value of a given metric.
    Useful to answer "which servers have the highest CPU?" or "top 10 services by memory usage?"
    The metric_name must be an exact metric name (e.g. 'cpu', 'used', 'rta').
    """
    logger.info("Executing tool get_top_resources_by_metric")
    return await TopMetricResult.get(metric_name)
