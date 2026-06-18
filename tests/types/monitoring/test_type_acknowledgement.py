from unittest.mock import AsyncMock, patch

from centreon_mcp.types.monitoring.acknowledgement import (
    Acknowledgement,
    AcknowledgementParams,
    AcknowledgementResource,
)

MODULE = "centreon_mcp.types.monitoring.acknowledgement"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_add_acknowledgement(request: AsyncMock):

    # Setup args
    params = AcknowledgementParams.model_construct()
    resources = [AcknowledgementResource.model_construct(host_id=10)]

    # Mock request
    request.return_value = None

    # Call test function
    await Acknowledgement.add(params, resources)

    # Assert request called with right args
    payload = {
        "acknowledgement": params.model_dump(mode="json"),
        "resources": [resource.dump() for resource in resources],
    }
    request.assert_awaited_once_with("POST", "monitoring/resources/acknowledge", payload=payload)


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_cancel_acknowledgement(request: AsyncMock):

    # Setup args
    with_services = True
    resources = [AcknowledgementResource.model_construct(host_id=10)]

    # Mock request
    request.return_value = None

    # Call test function
    await Acknowledgement.cancel(True, resources)

    # Assert request called with right args
    payload = {
        "disacknowledgement": {"with_services": with_services},
        "resources": [resource.dump() for resource in resources],
    }
    request.assert_awaited_once_with(
        "DELETE", "monitoring/resources/acknowledgements", payload=payload
    )
