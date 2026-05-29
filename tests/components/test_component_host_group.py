from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.host_group import (
    HostGroupConfigurationFilter,
    HostGroupConfigurationOrder,
    HostGroupFilter,
    HostGroupOrder,
    create_host_group_configuration,
    delete_host_group_configurations,
    list_host_group_configurations,
    list_host_groups,
    update_host_group_configuration,
)
from centreon_mcp.types.host_group import (
    Host,
    HostGroup,
    HostGroupConfiguration,
    HostGroupConfigurationFullParams,
    HostGroupConfigurationPartialParams,
    Icon,
)

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
    _list.assert_awaited_once_with(HostGroup, HostGroupOrder, filters, limit, page, order)

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
    _list.assert_awaited_once_with(
        HostGroupConfiguration, HostGroupConfigurationOrder, filters, limit, page, order
    )

    # Assert result
    assert results[0] == hostgroup_configuration


@patch(f"{MODULE}.HostGroupConfiguration.create", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_create_host_group_configuration(
    logger: MagicMock, hostgroup_configuration_create: AsyncMock
):

    # Setup args
    params = HostGroupConfigurationFullParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock HostGroupConfiguration.add
    hostgroup_configuration_create.return_value = True

    # Call test function
    result = await create_host_group_configuration(params)

    # Assert HostqgqroupConfiguration.add called with right args
    hostgroup_configuration_create.assert_awaited_once_with(params)

    # Assert result
    assert result


@patch(f"{MODULE}.HostGroupConfiguration.update", new_callable=AsyncMock)
@patch(f"{MODULE}.HostGroupConfiguration.get", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_update_host_group_configuration(
    logger: MagicMock,
    hostgroup_configuration_get: AsyncMock,
    hostgroup_configuration_update: AsyncMock,
):

    # Setup args
    hostgroup_id = 10
    params = HostGroupConfigurationPartialParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock HostGroupConfiguration.get
    hostgroup = HostGroupConfiguration.model_construct(
        id=1,
        name="HostGroup",
        icon=Icon.model_construct(id=1),
        hosts=[Host(id=10, name="host_name_10")],
    )
    hostgroup_configuration_get.return_value = hostgroup

    # Mock HostGroupConfiguration.update
    hostgroup_configuration_update.return_value = True

    # Call test function
    result = await update_host_group_configuration(hostgroup_id, params)

    # Assert HostGrougConfiguration.get called with right args
    hostgroup_configuration_get.assert_awaited_once_with(hostgroup_id)

    # Assert HostSeverity.update called with right args
    data = hostgroup.model_dump(exclude={"id", "is_activated", "icon", "hosts"})
    data["icon_id"] = hostgroup.icon.id if hostgroup.icon else None
    data["hosts"] = [host.id for host in hostgroup.hosts if host.id not in params.hosts_removed]
    data["hosts"] += [host_id for host_id in params.hosts_added if host_id not in data["hosts"]]
    data |= params.model_dump(exclude_none=True)
    hostgroup_configuration_update.assert_awaited_once_with(
        hostgroup_id, HostGroupConfigurationFullParams(**data)
    )

    # Assert result
    assert result


@patch(f"{MODULE}.HostGroupConfiguration.delete", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_delete_host_group_configurations(
    logger: MagicMock, hostgroup_configuration_delete: AsyncMock
):

    # Setup args
    hostgroup_id = 10

    # Mock logger
    logger.info.return_value = None

    # Mock HostGroupConfiguration.delete
    hostgroup_configuration_delete.return_value = True

    # Call test function
    result = await delete_host_group_configurations([hostgroup_id])

    # Assert HostConfigurationGroup.delete called with right args
    hostgroup_configuration_delete.assert_awaited_once_with(hostgroup_id)

    # Assert result
    assert result == {hostgroup_id: True}
