from unittest.mock import AsyncMock, MagicMock, call, patch

from centreon_mcp.components.monitoring_server import (
    generate_monitoring_servers_configurations,
    list_monitoring_servers,
    reload_monitoring_servers_configurations,
)
from centreon_mcp.types.monitoring.monitoring_server import (
    MonitoringServer,
    MonitoringServerFilter,
    MonitoringServerOrder,
)

MODULE = "centreon_mcp.components.monitoring_server"


@patch(f"{MODULE}.MonitoringServer.list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_monitoring_servers(logger: MagicMock, list_mixin: AsyncMock):

    # Setup args
    filters = [MonitoringServerFilter.model_construct()]
    limit = 50
    page = 1
    order = MonitoringServerOrder()

    # Mock logger
    logger.debug.return_value = None

    # Mock MonitoringServer.list
    monitoring_server = MonitoringServer.model_construct()
    list_mixin.return_value = [monitoring_server]

    # Call test function
    results = await list_monitoring_servers(filters, limit, page, order)

    # Assert MonitoringServer.list called with right args
    list_mixin.assert_awaited_once_with(filters, limit, page, order)

    # Assert result
    assert results[0] == monitoring_server


@patch(f"{MODULE}.MonitoringServerConfiguration.generate", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_generate_monitoring_servers_configurations(
    logger: MagicMock, monitoring_server_configuration_generate: AsyncMock
):

    # Setup args
    monitoring_servers_ids = [1, 2, 3]

    # Mock logger
    logger.debug.return_value = None

    # Mock MonitoringServerConfiguration.generate
    output = [True, True, True]
    monitoring_server_configuration_generate.side_effect = output

    # Call the test function
    results = await generate_monitoring_servers_configurations(monitoring_servers_ids)

    # Check MonitoringServerConfiguration.generate was called with right args
    monitoring_server_configuration_generate.assert_has_awaits(
        [call(monitoring_server_id) for monitoring_server_id in monitoring_servers_ids]
    )

    # Check results
    assert results == dict(zip(monitoring_servers_ids, output, strict=True))


@patch(f"{MODULE}.MonitoringServerConfiguration.generate", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_generate_monitoring_servers_configurations_all(
    logger: MagicMock, monitoring_server_configuration_generate: AsyncMock
):

    # Mock logger
    logger.debug.return_value = None

    # Mock MonitoringServerConfiguration.generate
    monitoring_server_configuration_generate.return_value = True

    # Call the test function
    result = await generate_monitoring_servers_configurations(None)

    # Check MonitoringServerConfiguration.generate was called with right args
    monitoring_server_configuration_generate.assert_awaited_once_with()

    # Check result
    assert result


@patch(f"{MODULE}.MonitoringServerConfiguration.reload", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_reload_monitoring_servers_configurations(
    logger: MagicMock, monitoring_server_configuration_reload: AsyncMock
):

    # Setup args
    monitoring_servers_ids = [1, 2, 3]

    # Mock logger
    logger.debug.return_value = None

    # Mock MonitoringServerConfiguration.reload
    output = [True, True, True]
    monitoring_server_configuration_reload.side_effect = output

    # Call the test function
    results = await reload_monitoring_servers_configurations(monitoring_servers_ids)

    # Check MonitoringServerConfiguration.reload was called with right args
    monitoring_server_configuration_reload.assert_has_awaits(
        [call(monitoring_server_id) for monitoring_server_id in monitoring_servers_ids]
    )

    # Check results
    assert results == dict(zip(monitoring_servers_ids, output, strict=True))


@patch(f"{MODULE}.MonitoringServerConfiguration.reload", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_reload_monitoring_servers_configurations_all(
    logger: MagicMock, monitoring_server_configuration_reload: AsyncMock
):

    # Mock logger
    logger.debug.return_value = None

    # Mock MonitoringServerConfiguration.reload
    monitoring_server_configuration_reload.return_value = True

    # Call the test function
    result = await reload_monitoring_servers_configurations(None)

    # Check MonitoringServerConfiguration.reload was called with right args
    monitoring_server_configuration_reload.assert_awaited_once_with()

    # Check result
    assert result
