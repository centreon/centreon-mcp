from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.check import request_check
from centreon_mcp.types.monitoring.check import CheckParams, CheckResource

MODULE = "centreon_mcp.components.check"


@patch(f"{MODULE}.Check.request", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_force_check_default(logger: MagicMock, submit: AsyncMock):

    # Setup args
    params = CheckParams.model_construct()
    resources = [CheckResource.model_construct(host_id=10)]

    # Mock logger
    logger.info.return_value = None

    # Mock Check.request
    submit.return_value = True

    # Call test function
    result = await request_check(resources, params)

    # Assert Check.request called with right args
    submit.assert_awaited_once_with(params, resources)

    # Assert result
    assert result
