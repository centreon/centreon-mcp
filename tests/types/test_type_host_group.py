from unittest.mock import AsyncMock, patch

from centreon_mcp.types.host_group import (
    HostGroupConfiguration,
)

MODULE = "centreon_mcp.types.host_group"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_hostgroup_configuration_get(request: AsyncMock):

    # Setup args
    hostgroup = HostGroupConfiguration.model_construct(
        id=10, name="Hostgroup", is_activated=True, enabled_hosts_count=10, disabled_hosts_count=10
    )

    # Mock request
    request.return_value = hostgroup.model_dump(mode="json")

    # Call test function
    result = await HostGroupConfiguration.get(hostgroup.id)

    # Assert request called with right args
    request.assert_awaited_once_with("GET", f"configuration/hosts/groups/{hostgroup.id}")

    # Check result
    assert result == hostgroup
