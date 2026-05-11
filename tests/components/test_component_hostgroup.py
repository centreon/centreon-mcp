from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.hostgroup import (
    HostGroupFilter,
    HostGroupOrder,
    list_hostgroups,
)
from centreon_mcp.types.hostgroup import HostGroup

MODULE = "centreon_mcp.components.hostgroup"


@patch(f"{MODULE}._list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_resources(logger: MagicMock, _list: AsyncMock):

    # Setup args
    filters = [HostGroupFilter.model_construct()]
    limit = 50
    page = 1
    order = HostGroupOrder()

    # Mock logger
    logger.debug.return_value = None

    # Mock _list
    hostgroup = HostGroup.model_construct()
    _list.return_value = [hostgroup]

    # Call test fonction
    results = await list_hostgroups(filters, limit, page, order)

    # Assert _list called with right args
    _list.assert_awaited_once_with(HostGroup, HostGroupOrder, filters, limit, page, order)

    # Assert result
    assert results[0] == hostgroup
