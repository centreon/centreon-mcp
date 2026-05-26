from unittest.mock import AsyncMock, patch

from centreon_mcp.types.host import (
    Host,
    HostConfiguration,
    HostConfigurationPartialParams,
    HostStatusCount,
)

MODULE = "centreon_mcp.types.host"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_host_count_by_status(request: AsyncMock):

    # Setup args
    search = ""

    # Mock request
    content: dict = {
        "up": {"total": 10},
        "down": {"total": 10},
        "unreachable": {"total": 10},
        "pending": {"total": 10},
        "total": 40,
    }
    request.return_value = content

    # Call test function
    result = await Host.count_by_status(search)

    # Assert request called with right args
    params = {"search": search}
    request.assert_awaited_once_with("GET", "monitoring/hosts/status", params=params)

    # Assert result
    assert result == HostStatusCount(**content)


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_host_configuration_patch(request: AsyncMock):

    # Setup args
    host_id = 10
    params = HostConfigurationPartialParams.model_construct()

    # Mock request
    request.return_value = None

    # Call test function
    await HostConfiguration.patch(host_id, params)

    # Assert request called with right args
    payload = params.model_dump(mode="json", exclude_none=True)
    request.assert_awaited_once_with("PATCH", f"configuration/hosts/{host_id}", payload)
