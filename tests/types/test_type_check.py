from unittest.mock import AsyncMock, patch

from centreon_mcp.types.check import Check, CheckResource

MODULE = "centreon_mcp.types.check"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_check_request(request: AsyncMock):

    # Setup args
    is_forced = True
    resources = [CheckResource.model_construct(host_id=10)]

    # Mock request
    request.return_value = None

    # Call test function
    await Check.request(is_forced, resources)

    # Assert request called with right args
    payload = {
        "check": {"is_forced": is_forced},
        "resources": [resource.dump() for resource in resources],
    }
    request.assert_awaited_once_with("POST", "monitoring/resources/check", payload=payload)
