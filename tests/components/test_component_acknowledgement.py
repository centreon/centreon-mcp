from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.acknowledgement import (
    cancel_acknowledgements,
    list_acknowledgements,
    set_acknowledgements,
)
from centreon_mcp.types.monitoring.acknowledgement import (
    Acknowledgement,
    AcknowledgementFilter,
    AcknowledgementOrder,
    AcknowledgementParams,
)
from centreon_mcp.utils.base import BaseResource

MODULE = "centreon_mcp.components.acknowledgement"


@patch(f"{MODULE}.Acknowledgement.list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_acknowledgements(logger: MagicMock, list_mixin: AsyncMock):

    # Setup args
    filters = [AcknowledgementFilter.model_construct()]
    limit = 50
    page = 1
    order = AcknowledgementOrder()

    # Mock logger
    logger.debug.return_value = None

    # Mock Acknowledgement.list
    acknowledgement = Acknowledgement.model_construct()
    list_mixin.return_value = [acknowledgement]

    # Call test function
    results = await list_acknowledgements(filters, limit, page, order)

    # Assert Acknowledgement.list called with right args
    list_mixin.assert_awaited_once_with(filters, limit, page, order)

    # Assert result
    assert results[0] == acknowledgement


@patch(f"{MODULE}.Acknowledgement.set", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_add_acknowledgements(logger: MagicMock, acknowledgement_set: AsyncMock):

    # Setup args
    params = AcknowledgementParams.model_construct()
    resources = [BaseResource.model_construct()]

    # Mock logger
    logger.info.return_value = None

    # Mock Acknowledgement.set
    acknowledgement_set.return_value = True

    # Call test function
    result = await set_acknowledgements(params, resources)

    # Assert Acknowledgement.set called with right args
    acknowledgement_set.assert_awaited_once_with(params, resources)

    # Assert result
    assert result


@patch(f"{MODULE}.Acknowledgement.cancel", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_cancel_acknowledgements(logger: MagicMock, cancel: AsyncMock):

    # Setup args
    with_services = True
    resources = [BaseResource.model_construct()]

    # Mock logger
    logger.info.return_value = None

    # Mock Acknowledgement.add
    cancel.return_value = True

    # Call test function
    result = await cancel_acknowledgements(with_services, resources)

    # Assert Acknowledgement.cancel called with right args
    cancel.assert_awaited_once_with(with_services, resources)

    # Assert result
    assert result
