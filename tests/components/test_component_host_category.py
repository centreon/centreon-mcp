from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.host_category import (
    HostCategoryConfigurationFilter,
    HostCategoryConfigurationOrder,
    create_host_category_configuration,
    delete_host_category_configurations,
    list_host_category_configurations,
    update_host_category_configuration,
)
from centreon_mcp.types.host_category import (
    HostCategoryConfiguration,
    HostCategoryConfigurationFullParams,
    HostCategoryConfigurationPartialParams,
)

MODULE = "centreon_mcp.components.host_category"


@patch(f"{MODULE}._list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_host_category_configurations(logger: MagicMock, _list: AsyncMock):

    # Setup args
    filters = [HostCategoryConfigurationFilter.model_construct()]
    limit = 50
    page = 1
    order = HostCategoryConfigurationOrder()

    # Mock logger
    logger.debug.return_value = None

    # Mock _list
    host_category_configuration = HostCategoryConfiguration.model_construct()
    _list.return_value = [host_category_configuration]

    # Call test fonction
    results = await list_host_category_configurations(filters, limit, page, order)

    # Assert _list called with right args
    _list.assert_awaited_once_with(
        HostCategoryConfiguration, HostCategoryConfigurationOrder, filters, limit, page, order
    )

    # Assert result
    assert results[0] == host_category_configuration


@patch(f"{MODULE}.HostCategoryConfiguration.create", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_create_host_category_configuration(
    logger: MagicMock, host_category_configuration_create: AsyncMock
):

    # Setup args
    params = HostCategoryConfigurationFullParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock HostCategoryConfiguration.create
    host_category_configuration_create.return_value = True

    # Call test function
    result = await create_host_category_configuration(params)

    # Assert HostCategoryConfiguration.create called with right args
    host_category_configuration_create.assert_awaited_once_with(params)

    # Assert result
    assert result


@patch(f"{MODULE}.HostCategoryConfiguration.update", new_callable=AsyncMock)
@patch(f"{MODULE}.HostCategoryConfiguration.get", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_update_host_category_configuration(
    logger: MagicMock,
    host_category_configuration_get: AsyncMock,
    host_category_configuration_update: AsyncMock,
):

    # Setup args
    host_category_id = 10
    params = HostCategoryConfigurationPartialParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock HostCategoryConfiguration.get
    host_category = HostCategoryConfiguration.model_construct(
        name="host_category_name", alias="host_category_alias"
    )
    host_category_configuration_get.return_value = host_category

    # Mock HostCategoryConfiguration.update
    host_category_configuration_update.return_value = True

    # Call test fonction
    result = await update_host_category_configuration(host_category_id, params)

    # Assert HostCategoryConfiguration.get called with right args
    host_category_configuration_get.assert_awaited_once_with(host_category_id)

    # Assert HostCategory.update called with right args
    data = host_category.model_dump(exclude={"id"}) | params.model_dump(exclude_none=True)
    host_category_configuration_update.assert_awaited_once_with(
        host_category_id, HostCategoryConfigurationFullParams(**data)
    )

    # Assert result
    assert result


@patch(f"{MODULE}.HostCategoryConfiguration.delete", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_delete_host_category_configurations(
    logger: MagicMock, host_category_configuration_delete: AsyncMock
):

    # Setup args
    host_category_id = 10

    # Mock logger
    logger.info.return_value = None

    # Mock HostCategoryConfiguration.delete
    host_category_configuration_delete.return_value = True

    # Call test fonction
    result = await delete_host_category_configurations([host_category_id])

    # Assert HostConfigurationCategory.delete called with right args
    host_category_configuration_delete.assert_awaited_once_with(host_category_id)

    # Assert result
    assert result == {host_category_id: True}
