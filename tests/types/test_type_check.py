from unittest.mock import AsyncMock, patch

from centreon_mcp.types.check import Check, CheckParams, CheckResource

MODULE = "centreon_mcp.types.check"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_check_request(request: AsyncMock):

    # Setup args
    params = CheckParams.model_construct()
    resources = [CheckResource.model_construct(host_id=10)]

    # Mock request
    request.return_value = None

    # Call test function
    await Check.request(params, resources)

    # Assert request called with right args
    payload = {
        "check": params.model_dump(mode="json"),
        "resources": [resource.dump() for resource in resources],
    }
    request.assert_awaited_once_with("POST", "monitoring/resources/check", payload=payload)
