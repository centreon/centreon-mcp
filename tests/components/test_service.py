import json
from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.service import ServiceFilter, count_services_by_status
from centreon_mcp.utils.type import ServiceStatusCount

MODULE = "centreon_mcp.components.service"


@patch(f"{MODULE}.Service.count_by_status", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_count_services_by_status(logger: MagicMock, count_by_status: AsyncMock):

    # Setup args
    filters = [ServiceFilter.model_construct()]

    # Mock logger
    logger.debug.return_value = None

    # Mock request
    count = ServiceStatusCount.model_construct()
    count_by_status.return_value = count

    # Call test fonction
    result = await count_services_by_status(filters)

    # Assert request called with right args
    conditions = (
        {
            "$or": [
                {"$and": filter.conditions} for filter in filters if filter.conditions
            ]
        }
        if filters
        else {}
    )
    count_by_status.assert_awaited_once_with(
        search=json.dumps(conditions),
    )

    # Assert result
    assert result == count
