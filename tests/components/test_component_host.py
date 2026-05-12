import json
from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.host import (
    HostConfigurationFilter,
    HostConfigurationOrder,
    HostFilter,
    count_hosts_by_status,
    create_host_configuration,
    delete_host_configurations,
    list_host_configurations,
    update_host_configuration,
)
from centreon_mcp.types.host import HostConfiguration, HostConfigurationParams, HostStatusCount

MODULE = "centreon_mcp.components.host"


@patch(f"{MODULE}.Host.count_by_status", new_callable=AsyncMock)
@patch(f"{MODULE}.HostFilter.join", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_count_hosts_by_status(
    logger: MagicMock, filter_join: MagicMock, host_count_by_status: AsyncMock
):

    # Setup args
    filters = [HostFilter.model_construct()]

    # Mock logger
    logger.debug.return_value = None

    # Mock HostFilter.join
    conditions: dict = {}
    filter_join.return_value = conditions

    # Mock request
    count = HostStatusCount.model_construct()
    host_count_by_status.return_value = count

    # Call test fonction
    result = await count_hosts_by_status(filters)

    # Assert request called with right args
    host_count_by_status.assert_awaited_once_with(json.dumps({}))

    # Assert result
    assert result == count


@patch(f"{MODULE}._list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_host_configurations(logger: MagicMock, _list: AsyncMock):

    # Setup args
    filters = [HostConfigurationFilter.model_construct()]
    limit = 50
    page = 1
    order = HostConfigurationOrder()

    # Mock logger
    logger.debug.return_value = None

    # Mock _list
    host_configuration = HostConfiguration.model_construct()
    _list.return_value = [host_configuration]

    # Call test fonction
    results = await list_host_configurations(filters, limit, page, order)

    # Assert _list called with right args
    _list.assert_awaited_once_with(
        HostConfiguration, HostConfigurationOrder, filters, limit, page, order
    )

    # Assert result
    assert results[0] == host_configuration


@patch(f"{MODULE}.HostConfiguration.create", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_create_host_configuration(logger: MagicMock, host_configuration_create: AsyncMock):

    # Setup args
    params = HostConfigurationParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock HostConfiguration.create
    host_configuration_create.return_value = None

    # Call test fonction
    result = await create_host_configuration(params)

    # Assert HostConfiguration.create called with right args
    host_configuration_create.assert_awaited_once_with(params)

    # Assert result
    assert result


@patch(f"{MODULE}.HostConfiguration.update", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_update_host_configuration(logger: MagicMock, host_configuration_update: AsyncMock):

    # Setup args
    host_id = 10
    params = HostConfigurationParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock HostConfiguration.update
    host_configuration_update.return_value = None

    # Call test fonction
    result = await update_host_configuration(host_id, params)

    # Assert HostConfiguration.update called with right args
    host_configuration_update.assert_awaited_once_with(host_id, params)

    # Assert result
    assert result


@patch(f"{MODULE}.HostConfiguration.delete", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_delete_host_configuration(logger: MagicMock, host_configuration_delete: AsyncMock):

    # Setup args
    host_id = 10

    # Mock logger
    logger.info.return_value = None

    # Mock HostConfiguration.delete
    host_configuration_delete.return_value = None

    # Call test fonction
    result = await delete_host_configurations([host_id])

    # Assert HostConfiguration.delete called with right args
    host_configuration_delete.assert_awaited_once_with(host_id)

    # Assert result
    assert result
