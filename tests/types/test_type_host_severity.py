from unittest.mock import AsyncMock, patch

from centreon_mcp.types.host_severity import HostSeverity, HostSeverityParams

MODULE = "centreon_mcp.types.host_severity"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_create_host_severity(request: AsyncMock):

    # Setup args
    params = HostSeverityParams.model_construct()

    # Mock request
    request.return_value = None

    # Call test function
    await HostSeverity.create(params)

    # Assert request called with right args
    payload = params.model_dump(mode="json")
    request.assert_awaited_once_with("POST", "configuration/hosts/severities", payload)


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_delete_host_severity(request: AsyncMock):

    # Setup args
    host_severity_id = 10

    # Mock request
    request.return_value = None

    # Call test function
    await HostSeverity.delete(host_severity_id)

    # Assert request called with right args
    request.assert_awaited_once_with("DELETE", f"configuration/hosts/severities/{host_severity_id}")
