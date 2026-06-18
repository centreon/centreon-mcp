import json
from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.host import (
    count_hosts_by_status,
    create_host_configuration,
    delete_host_configurations,
    list_host_configurations,
    update_host_configuration,
)
from centreon_mcp.types.configuration.host import (
    HostConfiguration,
    HostConfigurationFilter,
    HostConfigurationFullParams,
    HostConfigurationOrder,
    HostConfigurationPartialParams,
)
from centreon_mcp.types.monitoring.host import HostFilter, HostStatusCount

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

    # Call test function
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

    # Call test function
    results = await list_host_configurations(filters, limit, page, order)

    # Assert _list called with right args
    _list.assert_awaited_once_with(HostConfiguration, filters, limit, page, order)

    # Assert result
    assert results[0] == host_configuration


@patch(f"{MODULE}._create", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_create_host_configuration(logger: MagicMock, _create: AsyncMock):

    # Setup args
    params = HostConfigurationFullParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock _create
    _create.return_value = True

    # Call test function
    result = await create_host_configuration(params)

    # Assert _create called with right args
    _create.assert_awaited_once_with(HostConfiguration, params)

    # Assert result
    assert result


@patch(f"{MODULE}._patch", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_update_host_configuration(logger: MagicMock, _patch: AsyncMock):

    # Setup args
    host_id = 10
    params = HostConfigurationPartialParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock _patch
    _patch.return_value = True

    # Call test function
    result = await update_host_configuration(host_id, params)

    # Assert _patch called with right args
    _patch.assert_awaited_once_with(HostConfiguration, host_id, params)

    # Assert result
    assert result


@patch(f"{MODULE}._delete", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_delete_host_configurations(logger: MagicMock, _delete: AsyncMock):

    # Setup args
    host_id = 10

    # Mock logger
    logger.info.return_value = None

    # Mock _delete
    _delete.return_value = {host_id: True}

    # Call test function
    result = await delete_host_configurations([host_id])

    # Assert _delete called with right args
    _delete.assert_awaited_once_with(HostConfiguration, [host_id])

    # Assert result
    assert result == {host_id: True}
