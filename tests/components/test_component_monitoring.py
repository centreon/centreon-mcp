from typing import Literal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from centreon_mcp.components.monitoring import list_monitoring_entities

MODULE = "centreon_mcp.components.monitoring"


@pytest.mark.parametrize(
    "model_type",
    [
        "host_group",
        "service_group",
        "monitoring_server",
    ],
)
@patch("centreon_mcp.utils.mixins.ListMixin.list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_monitoring_entities(
    logger: MagicMock,
    list_mixin: AsyncMock,
    model_type: Literal[
        "host_group",
        "service_group",
        "monitoring_server",
    ],
):

    # Setup args
    filters = [MagicMock()]
    limit = 50
    page = 1
    order = MagicMock()

    # Mock logger
    logger.debug.return_value = None

    model = MagicMock()
    list_mixin.return_value = [model]

    # Call test function
    results = await list_monitoring_entities(model_type, filters, limit, page, order)

    # Assert ListMixin.list called with right args
    list_mixin.assert_awaited_once_with(filters, limit, page, order)

    # Assert result
    assert results == [model]
