from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.servicegroup import list_servicegroups
from centreon_mcp.types.monitoring.servicegroup import (
    ServiceGroup,
    ServiceGroupFilter,
    ServiceGroupOrder,
)

MODULE = "centreon_mcp.components.servicegroup"


@patch(f"{MODULE}.ServiceGroup.list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_servicegroups(logger: MagicMock, list_mixin: AsyncMock):

    # Setup args
    filters = [ServiceGroupFilter.model_construct()]
    limit = 50
    page = 1
    order = ServiceGroupOrder()

    # Mock logger
    logger.debug.return_value = None

    # Mock ServiceGroup.list
    servicegroup = ServiceGroup.model_construct()
    list_mixin.return_value = [servicegroup]

    # Call test function
    results = await list_servicegroups(filters, limit, page, order)

    # Assert ServiceGroup.list called with right args
    list_mixin.assert_awaited_once_with(filters, limit, page, order)

    # Assert result
    assert results[0] == servicegroup
