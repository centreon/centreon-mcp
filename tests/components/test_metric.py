from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from centreon_mcp.components.metric import (
    get_metric_performance_data,
    get_service_metrics,
    get_top_resources_by_metric,
)
from centreon_mcp.utils.type import Metric, MetricSeries, PerformanceData, TopMetricResult

MODULE = "centreon_mcp.components.metric"


@patch(f"{MODULE}.Metric.list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_get_service_metrics(logger: MagicMock, metric_list: AsyncMock):

    # Setup args
    host_id = 12
    service_id = 5

    # Mock logger
    logger.info.return_value = None

    # Mock Metric.list
    metrics = [Metric.model_construct(id=1, name="rta", unit="ms", current_value=0.025)]
    metric_list.return_value = metrics

    # Call test function
    result = await get_service_metrics(host_id, service_id)

    # Assert Metric.list called with right args
    metric_list.assert_awaited_once_with(host_id, service_id)

    # Assert result
    assert result == metrics


@patch(f"{MODULE}.PerformanceData.get", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_get_metric_performance_data(logger: MagicMock, perf_get: AsyncMock):

    # Setup args
    host_id = 12
    service_id = 5
    start = "2024-01-15T08:00:00Z"
    end = "2024-01-15T20:00:00Z"

    # Mock logger
    logger.info.return_value = None

    # Mock PerformanceData.get
    perf_data = PerformanceData.model_construct(
        base=1024,
        metrics=[MetricSeries.model_construct(metric_id=1, metric="used", unit="B", data=[100.0])],
        times=["1705305600"],
    )
    perf_get.return_value = perf_data

    # Call test function
    result = await get_metric_performance_data(host_id, service_id, start, end)

    # Assert PerformanceData.get called with right args
    perf_get.assert_awaited_once_with(host_id, service_id, start, end)

    # Assert result
    assert result == perf_data


@patch(f"{MODULE}.PerformanceData.get", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_get_metric_performance_data_no_dates(logger: MagicMock, perf_get: AsyncMock):

    # Setup args
    host_id = 12
    service_id = 5

    # Mock logger
    logger.info.return_value = None

    # Mock PerformanceData.get
    perf_data = PerformanceData.model_construct(base=1000, metrics=[], times=[])
    perf_get.return_value = perf_data

    # Call test function (no start/end)
    result = await get_metric_performance_data(host_id, service_id)

    # Assert PerformanceData.get called with None dates
    perf_get.assert_awaited_once_with(host_id, service_id, None, None)

    # Assert result
    assert result == perf_data


@patch(f"{MODULE}.PerformanceData.get", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_get_metric_performance_data_invalid_start(logger: MagicMock, perf_get: AsyncMock):

    # Mock logger
    logger.info.return_value = None

    # Call test function with invalid date format
    with pytest.raises(ValueError):
        await get_metric_performance_data(12, 5, "not-a-date", None)

    # Assert PerformanceData.get was NOT called (validation failed before)
    perf_get.assert_not_awaited()


@patch(f"{MODULE}.PerformanceData.get", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_get_metric_performance_data_invalid_end(logger: MagicMock, perf_get: AsyncMock):

    # Mock logger
    logger.info.return_value = None

    # Call test function with invalid end date
    with pytest.raises(ValueError):
        await get_metric_performance_data(12, 5, "2024-01-15T08:00:00Z", "garbage")

    # Assert PerformanceData.get was NOT called
    perf_get.assert_not_awaited()


@patch(f"{MODULE}.TopMetricResult.get", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_get_top_resources_by_metric(logger: MagicMock, top_get: AsyncMock):

    # Setup args
    metric_name = "cpu"

    # Mock logger
    logger.info.return_value = None

    # Mock TopMetricResult.get
    top_result = TopMetricResult.model_construct(
        name="cpu", unit="%", sort="top", limit=10, resources=[]
    )
    top_get.return_value = top_result

    # Call test function
    result = await get_top_resources_by_metric(metric_name)

    # Assert TopMetricResult.get called with right args
    top_get.assert_awaited_once_with(metric_name)

    # Assert result
    assert result == top_result
