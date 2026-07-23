from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.check import request_check
from centreon_mcp.types.monitoring.actions.check import CheckParams
from centreon_mcp.utils.base import BaseResource

MODULE = "centreon_mcp.components.check"


@patch(f"{MODULE}.Check.set", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_force_check_default(logger: MagicMock, check_set: AsyncMock):

    # Setup args
    params = CheckParams.model_construct()
    resources = [BaseResource.model_construct(host_id=10)]

    # Mock logger
    logger.info.return_value = None

    # Mock Check.set
    check_set.return_value = True

    # Call test function
    result = await request_check(resources, params)

    # Assert Check.set called with right args
    check_set.assert_awaited_once_with(params, resources)

    # Assert result
    assert result
