from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.host_group import (
    list_host_groups,
)
from centreon_mcp.types.monitoring.host_group import HostGroup, HostGroupFilter, HostGroupOrder

MODULE = "centreon_mcp.components.host_group"


@patch(f"{MODULE}.HostGroup.list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_resources(logger: MagicMock, list_mixin: AsyncMock):

    # Setup args
    filters = [HostGroupFilter.model_construct()]
    limit = 50
    page = 1
    order = HostGroupOrder()

    # Mock logger
    logger.debug.return_value = None

    # Mock HostGroup.list
    hostgroup = HostGroup.model_construct()
    list_mixin.return_value = [hostgroup]

    # Call test function
    results = await list_host_groups(filters, limit, page, order)

    # Assert HostGroup.list called with right args
    list_mixin.assert_awaited_once_with(filters, limit, page, order)

    # Assert result
    assert results[0] == hostgroup
