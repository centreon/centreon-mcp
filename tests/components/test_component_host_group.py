from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.host_group import (
    create_host_group_configuration,
    delete_host_group_configurations,
    list_host_group_configurations,
    list_host_groups,
    update_host_group_configuration,
)
from centreon_mcp.types.configuration.host_group import (
    HostGroupConfiguration,
    HostGroupConfigurationFilter,
    HostGroupConfigurationFullParams,
    HostGroupConfigurationOrder,
    HostGroupConfigurationPartialParams,
)
from centreon_mcp.types.monitoring.host_group import HostGroup, HostGroupFilter, HostGroupOrder

MODULE = "centreon_mcp.components.host_group"


@patch(f"{MODULE}._list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_resources(logger: MagicMock, _list: AsyncMock):

    # Setup args
    filters = [HostGroupFilter.model_construct()]
    limit = 50
    page = 1
    order = HostGroupOrder()

    # Mock logger
    logger.debug.return_value = None

    # Mock _list
    hostgroup = HostGroup.model_construct()
    _list.return_value = [hostgroup]

    # Call test function
    results = await list_host_groups(filters, limit, page, order)

    # Assert _list called with right args
    _list.assert_awaited_once_with(HostGroup, filters, limit, page, order)

    # Assert result
    assert results[0] == hostgroup


@patch(f"{MODULE}._list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_host_group_configurations(logger: MagicMock, _list: AsyncMock):

    # Setup args
    filters = [HostGroupConfigurationFilter.model_construct()]
    limit = 50
    page = 1
    order = HostGroupConfigurationOrder()

    # Mock logger
    logger.debug.return_value = None

    # Mock _list
    hostgroup_configuration = HostGroupConfiguration.model_construct()
    _list.return_value = [hostgroup_configuration]

    # Call test function
    results = await list_host_group_configurations(filters, limit, page, order)

    # Assert _list called with right args
    _list.assert_awaited_once_with(HostGroupConfiguration, filters, limit, page, order)

    # Assert result
    assert results[0] == hostgroup_configuration


@patch(f"{MODULE}._create", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_create_host_group_configuration(logger: MagicMock, _create: AsyncMock):

    # Setup args
    params = HostGroupConfigurationFullParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock _create
    _create.return_value = True

    # Call test function
    result = await create_host_group_configuration(params)

    # Assert _create called with right args
    _create.assert_awaited_once_with(HostGroupConfiguration, params)

    # Assert result
    assert result


@patch(f"{MODULE}._update", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_update_host_severity(logger: MagicMock, _update: AsyncMock):

    # Setup args
    host_group_id = 10
    params = HostGroupConfigurationPartialParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock _update
    _update.return_value = True

    # Call test function
    result = await update_host_group_configuration(host_group_id, params)

    # Assert _update called with right args
    _update.assert_awaited_once_with(
        HostGroupConfiguration, HostGroupConfigurationFullParams, host_group_id, params
    )

    # Assert result
    assert result


@patch(f"{MODULE}._delete", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_delete_host_group_configurations(logger: MagicMock, _delete: AsyncMock):

    # Setup args
    hostgroup_id = 10

    # Mock logger
    logger.info.return_value = None

    # Mock _delete
    _delete.return_value = {hostgroup_id: True}

    # Call test function
    result = await delete_host_group_configurations([hostgroup_id])

    # Assert _delete called with right args
    _delete.assert_awaited_once_with(HostGroupConfiguration, [hostgroup_id])

    # Assert result
    assert result == {hostgroup_id: True}
