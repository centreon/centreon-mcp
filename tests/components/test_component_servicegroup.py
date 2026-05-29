from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.servicegroup import (
    ServiceGroupFilter,
    ServiceGroupOrder,
    list_servicegroups,
)
from centreon_mcp.types.servicegroup import ServiceGroup

MODULE = "centreon_mcp.components.servicegroup"


@patch(f"{MODULE}._list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_servicegroups(logger: MagicMock, _list: AsyncMock):

    # Setup args
    filters = [ServiceGroupFilter.model_construct()]
    limit = 50
    page = 1
    order = ServiceGroupOrder()

    # Mock logger
    logger.debug.return_value = None

    # Mock _list
    servicegroup = ServiceGroup.model_construct()
    _list.return_value = [servicegroup]

    # Call test function
    results = await list_servicegroups(filters, limit, page, order)

    # Assert _list called with right args
    _list.assert_awaited_once_with(ServiceGroup, ServiceGroupOrder, filters, limit, page, order)

    # Assert result
    assert results[0] == servicegroup
