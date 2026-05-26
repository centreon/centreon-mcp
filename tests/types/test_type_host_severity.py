from unittest.mock import AsyncMock, patch

from centreon_mcp.types.host_severity import (
    HostSeverity,
    HostSeverityFullParams,
)

MODULE = "centreon_mcp.types.host_severity"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_get_host_severity(request: AsyncMock):

    # Setup args
    host_severity_id = 10

    # Mock request
    host_severity = HostSeverity.model_construct(
        id=host_severity_id, name="Name", alias="Alias", level=10, icon_id=1, is_activated=True
    )
    request.return_value = host_severity.model_dump(mode="json")

    # Call test function
    result = await HostSeverity.get(host_severity_id)

    # Assert request called with right args
    request.assert_awaited_once_with("GET", f"configuration/hosts/severities/{host_severity_id}")

    # Assert result
    assert result == host_severity


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_update_host_severity(request: AsyncMock):

    # Setup args
    host_severity_id = 10
    params = HostSeverityFullParams.model_construct()

    # Mock request
    request.return_value = None

    # Call test function
    await HostSeverity.update(host_severity_id, params)

    # Assert request called with right args
    payload = params.model_dump(mode="json", exclude_none=True)
    request.assert_awaited_once_with(
        "PUT", f"configuration/hosts/severities/{host_severity_id}", payload
    )


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
