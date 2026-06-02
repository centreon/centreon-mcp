from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.monitoring_server import (
    MonitoringServerFilter,
    MonitoringServerOrder,
    list_monitoring_servers,
)
from centreon_mcp.types.monitoring_server import MonitoringServer

MODULE = "centreon_mcp.components.monitoring_server"


@patch(f"{MODULE}._list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_monitoring_servers(logger: MagicMock, _list: AsyncMock):

    # Setup args
    filters = [MonitoringServerFilter.model_construct()]
    limit = 50
    page = 1
    order = MonitoringServerOrder()

    # Mock logger
    logger.debug.return_value = None

    # Mock _list
    monitoring_server = MonitoringServer.model_construct()
    _list.return_value = [monitoring_server]

    # Call test function
    results = await list_monitoring_servers(filters, limit, page, order)

    # Assert _list called with right args
    _list.assert_awaited_once_with(MonitoringServer, filters, limit, page, order)

    # Assert result
    assert results[0] == monitoring_server
