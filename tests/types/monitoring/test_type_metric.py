from unittest.mock import AsyncMock, patch

from centreon_mcp.types.monitoring.metric import Metric

MODULE = "centreon_mcp.types.monitoring.metric"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_metric_list(request: AsyncMock):

    # Setup args
    host_id = 12
    service_id = 5

    # Mock request
    content = [
        {
            "id": 1,
            "name": "rta",
            "unit": "ms",
            "current_value": 0.025,
            "warning_high_threshold": 200.0,
            "warning_low_threshold": None,
            "critical_high_threshold": 400.0,
            "critical_low_threshold": None,
        },
        {
            "id": 2,
            "name": "pl",
            "unit": "%",
            "current_value": 0.0,
            "warning_high_threshold": 20.0,
            "warning_low_threshold": None,
            "critical_high_threshold": 50.0,
            "critical_low_threshold": None,
        },
    ]
    request.return_value = content

    # Call test function
    result = await Metric.list(host_id, service_id)

    # Assert request called with right args
    endpoint = f"monitoring/hosts/{host_id}/services/{service_id}/metrics"
    request.assert_awaited_once_with("GET", endpoint)

    # Assert result
    assert len(result) == 2
    assert result[0].name == "rta"
    assert result[0].unit == "ms"
    assert result[0].current_value == 0.025
    assert result[1].name == "pl"
    assert result[1].critical_high_threshold == 50.0
