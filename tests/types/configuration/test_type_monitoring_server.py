from unittest.mock import AsyncMock, patch

import pytest

from centreon_mcp.types.configuration.monitoring_server import MonitoringServer

MODULE = "centreon_mcp.types.configuration.monitoring_server"


@pytest.mark.parametrize(
    "monitoring_server_id,endpoint",
    [
        (10, "configuration/monitoring-servers/10/generate"),
        (None, "configuration/monitoring-servers/generate"),
    ],
)
@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_monitoring_server_configuration_generate(
    request: AsyncMock, monitoring_server_id: int | None, endpoint: str
):

    # Mock request
    request.return_value = None

    # Call test function
    await MonitoringServer.generate(monitoring_server_id)

    # Assert request called with right args
    request.assert_awaited_once_with("GET", endpoint)


@pytest.mark.parametrize(
    "monitoring_server_id,endpoint",
    [
        (10, "configuration/monitoring-servers/10/reload"),
        (None, "configuration/monitoring-servers/reload"),
    ],
)
@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_monitoring_server_configuration_reaload(
    request: AsyncMock, monitoring_server_id: int | None, endpoint: str
):

    # Mock request
    request.return_value = None

    # Call test function
    await MonitoringServer.reload(monitoring_server_id)

    # Assert request called with right args
    request.assert_awaited_once_with("GET", endpoint)
