import json
from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.service import ServiceFilter, count_services_by_status
from centreon_mcp.types.service import ServiceStatusCount

MODULE = "centreon_mcp.components.service"


@patch(f"{MODULE}.Service.count_by_status", new_callable=AsyncMock)
@patch(f"{MODULE}.ServiceFilter.join", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_count_services_by_status(
    logger: MagicMock, filter_join: MagicMock, service_count_by_status: AsyncMock
):

    # Setup args
    filters = [ServiceFilter.model_construct()]

    # Mock logger
    logger.debug.return_value = None

    # Mock ServiceFilter.join
    conditions: dict = {}
    filter_join.return_value = conditions

    # Mock request
    count = ServiceStatusCount.model_construct()
    service_count_by_status.return_value = count

    # Call test function
    result = await count_services_by_status(filters)

    # Assert request called with right args
    service_count_by_status.assert_awaited_once_with(json.dumps({}))

    # Assert result
    assert result == count
