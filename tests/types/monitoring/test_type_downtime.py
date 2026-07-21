from unittest.mock import AsyncMock, patch

from centreon_mcp.types.monitoring.downtime import Downtime, DowntimeParams
from centreon_mcp.utils.base import BaseResource

MODULE = "centreon_mcp.types.monitoring.downtime"


@patch(f"{MODULE}.Downtime._set", new_callable=AsyncMock)
async def test_set_downtime(_set_mixin: AsyncMock):

    # Setup args
    params = DowntimeParams.model_construct()
    resources = [BaseResource.model_construct(host_id=10)]

    # Mock SetMixin._set
    _set_mixin.return_value = None

    # Call test function
    await Downtime.set(params, resources)

    # Assert SetMixin._set called with right args
    _set_mixin.assert_awaited_once_with("monitoring/resources/downtime", params, resources)
