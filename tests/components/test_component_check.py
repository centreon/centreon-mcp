from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.check import request_check
from centreon_mcp.types.check import CheckResource

MODULE = "centreon_mcp.components.check"


@patch(f"{MODULE}.Check.request", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_force_check_default(logger: MagicMock, submit: AsyncMock):

    # Setup args
    is_forced = True
    resources = [CheckResource.model_construct(host_id=10)]

    # Mock logger
    logger.info.return_value = None

    # Mock Check.request
    submit.return_value = None

    # Call test function
    result = await request_check(resources, is_forced)

    # Assert Check.request called with right args
    submit.assert_awaited_once_with(is_forced, resources)

    # Assert result
    assert result
