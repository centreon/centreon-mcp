from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.downtime import cancel_downtimes, list_downtimes, set_downtimes
from centreon_mcp.types.monitoring.actions.downtime import (
    Downtime,
    DowntimeFilter,
    DowntimeOrder,
    DowntimeParams,
)
from centreon_mcp.utils.base import BaseResource

MODULE = "centreon_mcp.components.downtime"


@patch(f"{MODULE}.Downtime.list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_downtimes(logger: MagicMock, list_mixin: AsyncMock):

    # Setup args
    filters = [DowntimeFilter.model_construct()]
    limit = 50
    page = 1
    order = DowntimeOrder()

    # Mock logger
    logger.info.return_value = None

    # Mock Downtime.list
    downtime = Downtime.model_construct()
    list_mixin.return_value = [downtime]

    # Call test function
    results = await list_downtimes(filters, limit, page, order)

    # Assert Downtime.list called with right args
    list_mixin.assert_awaited_once_with(filters, limit, page, order)

    # Assert result
    assert results[0] == downtime


@patch(f"{MODULE}.Downtime.set", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_set_downtime(logger: MagicMock, downtime_set: AsyncMock):

    # Setup args
    params = DowntimeParams.model_construct()
    resources = [BaseResource.model_construct()]

    # Mock logger
    logger.info.return_value = None

    # Mock Downtime.set
    downtime_set.return_value = True

    # Call test function
    result = await set_downtimes(params, resources)

    # Assert Downtime.set called with right args
    downtime_set.assert_awaited_once_with(params, resources)

    # Assert result
    assert result


@patch(f"{MODULE}.Downtime.delete", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_cancel_downtimes(logger: MagicMock, delete: AsyncMock):

    # Setup args
    downtime_id = 10

    # Mock logger
    logger.info.return_value = None

    # Mock Downtime.delete
    delete.return_value = {downtime_id: True}

    # Call test function
    results = await cancel_downtimes([downtime_id])

    # Assert Downtime.delete called with right args
    delete.assert_awaited_once_with([downtime_id])

    # Assert result
    assert results == {downtime_id: True}
