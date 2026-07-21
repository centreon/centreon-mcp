from unittest.mock import AsyncMock, patch

from centreon_mcp.types.monitoring.acknowledgement import Acknowledgement, AcknowledgementParams
from centreon_mcp.utils.base import BaseResource

MODULE = "centreon_mcp.types.monitoring.acknowledgement"


@patch(f"{MODULE}.Acknowledgement._set", new_callable=AsyncMock)
async def test_set_acknowledgement(_set_mixin: AsyncMock):

    # Setup args
    params = AcknowledgementParams.model_construct()
    resources = [BaseResource.model_construct(host_id=10)]

    # Mock SetMixin._set
    _set_mixin.return_value = None

    # Call test function
    await Acknowledgement.set(params, resources)

    # Assert SetMixin._set called with right args
    _set_mixin.assert_awaited_once_with("monitoring/resources/acknowledge", params, resources)


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_cancel_acknowledgement(request: AsyncMock):

    # Setup args
    with_services = True
    resources = [BaseResource.model_construct(host_id=10)]

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
