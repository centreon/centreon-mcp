from unittest.mock import AsyncMock, MagicMock, call, patch

from centreon_mcp.components.monitoring_server import (
    generate_monitoring_servers_configurations,
    reload_monitoring_servers_configurations,
)

MODULE = "centreon_mcp.components.monitoring_server"


@patch(f"{MODULE}.MonitoringServer.generate", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_generate_monitoring_servers_configurations(
    logger: MagicMock, monitoring_server_configuration_generate: AsyncMock
):

    # Setup args
    monitoring_servers_ids = [1, 2, 3]

    # Mock logger
    logger.debug.return_value = None

    # Mock MonitoringServer.generate
    output = [True, True, True]
    monitoring_server_configuration_generate.side_effect = output

    # Call the test function
    results = await generate_monitoring_servers_configurations(monitoring_servers_ids)

    # Check MonitoringServer.generate was called with right args
    monitoring_server_configuration_generate.assert_has_awaits(
        [call(monitoring_server_id) for monitoring_server_id in monitoring_servers_ids]
    )

    # Check results
    assert results == dict(zip(monitoring_servers_ids, output, strict=True))


@patch(f"{MODULE}.MonitoringServer.generate", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_generate_monitoring_servers_configurations_all(
    logger: MagicMock, monitoring_server_configuration_generate: AsyncMock
):

    # Mock logger
    logger.debug.return_value = None

    # Mock MonitoringServer.generate
    monitoring_server_configuration_generate.return_value = True

    # Call the test function
    result = await generate_monitoring_servers_configurations(None)

    # Check MonitoringServer.generate was called with right args
    monitoring_server_configuration_generate.assert_awaited_once_with()

    # Check result
    assert result


@patch(f"{MODULE}.MonitoringServer.reload", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_reload_monitoring_servers_configurations(
    logger: MagicMock, monitoring_server_configuration_reload: AsyncMock
):

    # Setup args
    monitoring_servers_ids = [1, 2, 3]

    # Mock logger
    logger.debug.return_value = None

    # Mock MonitoringServer.reload
    output = [True, True, True]
    monitoring_server_configuration_reload.side_effect = output

    # Call the test function
    results = await reload_monitoring_servers_configurations(monitoring_servers_ids)

    # Check MonitoringServer.reload was called with right args
    monitoring_server_configuration_reload.assert_has_awaits(
        [call(monitoring_server_id) for monitoring_server_id in monitoring_servers_ids]
    )

    # Check results
    assert results == dict(zip(monitoring_servers_ids, output, strict=True))


@patch(f"{MODULE}.MonitoringServer.reload", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_reload_monitoring_servers_configurations_all(
    logger: MagicMock, monitoring_server_configuration_reload: AsyncMock
):

    # Mock logger
    logger.debug.return_value = None

    # Mock MonitoringServer.reload
    monitoring_server_configuration_reload.return_value = True

    # Call the test function
    result = await reload_monitoring_servers_configurations(None)

    # Check MonitoringServer.reload was called with right args
    monitoring_server_configuration_reload.assert_awaited_once_with()

    # Check result
    assert result
