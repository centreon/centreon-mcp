from unittest.mock import AsyncMock, patch

from centreon_mcp.types.monitoring.service import Service, ServiceStatusCount

MODULE = "centreon_mcp.types.monitoring.service"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_service_count_by_status(request: AsyncMock):

    # Setup args
    search = ""

    # Mock request
    content: dict = {
        "ok": {"total": 10},
        "warning": {"total": 10},
        "critical": {"total": 10},
        "unknown": {"total": 10},
        "pending": {"total": 10},
        "total": 50,
    }
    request.return_value = content

    # Call test function
    result = await Service.count_by_status(search)

    # Assert request called with right args
    params = {"search": search}
    request.assert_awaited_once_with("GET", "monitoring/services/status", params=params)

    # Assert result
    assert result == ServiceStatusCount(**content)
