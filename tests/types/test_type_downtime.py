from unittest.mock import AsyncMock, patch

from centreon_mcp.types.downtime import Downtime, DowntimeParams, DowntimeResource

MODULE = "centreon_mcp.types.downtime"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_set_downtime(request: AsyncMock):

    # Setup args
    params = DowntimeParams.model_construct()
    resources = [DowntimeResource.model_construct(host_id=10)]

    # Mock request
    request.return_value = None

    # Call test function
    await Downtime.set(params, resources)

    # Assert request called with right args
    payload = {
        "downtime": params.model_dump(mode="json"),
        "resources": [resource.dump() for resource in resources],
    }
    request.assert_awaited_once_with("POST", "monitoring/resources/downtime", payload=payload)


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_cancel_downtime(request: AsyncMock):

    # Setup args
    downtime_id = 10

    # Mock request
    request.return_value = None

    # Call test function
    await Downtime.cancel(downtime_id)

    # Assert request called with right args
    request.assert_awaited_once_with("DELETE", f"monitoring/downtimes/{downtime_id}")
