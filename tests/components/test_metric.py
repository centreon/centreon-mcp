from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.metric import get_service_metrics
from centreon_mcp.utils.type import Metric

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
    metrics = [
        Metric(
            id=1,
            name="rta",
            unit="ms",
            current_value=0.025,
            warning_high_threshold=200.0,
            warning_low_threshold=None,
            critical_high_threshold=400.0,
            critical_low_threshold=None,
        ),
        Metric(
            id=2,
            name="pl",
            unit="%",
            current_value=0.0,
            warning_high_threshold=20.0,
            warning_low_threshold=None,
            critical_high_threshold=50.0,
            critical_low_threshold=None,
        ),
    ]
    metric_list.return_value = metrics

    # Call test function
    results = await get_service_metrics(host_id, service_id)

    # Assert Metric.list called with right args
    metric_list.assert_awaited_once_with(host_id, service_id)

    # Assert result
    assert len(results) == 2
    assert results[0].name == "rta"
    assert results[1].name == "pl"
