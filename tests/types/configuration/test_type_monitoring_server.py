from typing import Literal
from unittest.mock import AsyncMock, patch

import pytest

from centreon_mcp.types.configuration.monitoring_server import MonitoringServer

MODULE = "centreon_mcp.types.configuration.monitoring_server"


@pytest.mark.parametrize(
    "action,monitoring_server_id,endpoint",
    [
        ("generate", 10, "configuration/monitoring-servers/10/generate"),
        ("generate", None, "configuration/monitoring-servers/generate"),
        ("reload", 10, "configuration/monitoring-servers/10/reload"),
        ("reload", None, "configuration/monitoring-servers/reload"),
    ],
)
@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_monitoring_server_manage(
    request: AsyncMock,
    action: Literal["generate", "reload"],
    monitoring_server_id: int | None,
    endpoint: str,
):

    # Mock request
    request.return_value = None

    # Call test function
    await MonitoringServer.manage(action, monitoring_server_id)

    # Assert request called with right args
    request.assert_awaited_once_with("GET", endpoint)
