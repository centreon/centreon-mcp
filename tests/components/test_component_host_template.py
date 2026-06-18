from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.host_template import (
    create_host_template,
    delete_host_templates,
    list_host_templates,
    update_host_template,
)
from centreon_mcp.types.configuration.host_template import (
    HostTemplate,
    HostTemplateFilter,
    HostTemplateFullParams,
    HostTemplateOrder,
    HostTemplatePartialParams,
)

MODULE = "centreon_mcp.components.host_template"


@patch(f"{MODULE}._list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_host_templates(logger: MagicMock, _list: AsyncMock):

    # Setup args
    filters = [HostTemplateFilter.model_construct()]
    limit = 50
    page = 1
    order = HostTemplateOrder()

    # Mock logger
    logger.debug.return_value = None

    # Mock _list
    host_template = HostTemplate.model_construct()
    _list.return_value = [host_template]

    # Call test function
    results = await list_host_templates(filters, limit, page, order)

    # Assert _list called with right args
    _list.assert_awaited_once_with(HostTemplate, filters, limit, page, order)

    # Assert result
    assert results[0] == host_template


@patch(f"{MODULE}._create", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_create_host_template(logger: MagicMock, _create: AsyncMock):

    # Setup args
    params = HostTemplateFullParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock _create
    _create.return_value = True

    # Call test function
    result = await create_host_template(params)

    # Assert _create called with right args
    _create.assert_awaited_once_with(HostTemplate, params)

    # Assert result
    assert result


@patch(f"{MODULE}._patch", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_update_host_template(logger: MagicMock, _patch: AsyncMock):

    # Setup args
    host_id = 10
    params = HostTemplatePartialParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock _patch
    _patch.return_value = True

    # Call test function
    result = await update_host_template(host_id, params)

    # Assert _patch called with right args
    _patch.assert_awaited_once_with(HostTemplate, host_id, params)

    # Assert result
    assert result


@patch(f"{MODULE}._delete", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_delete_host_templates(logger: MagicMock, _delete: AsyncMock):

    # Setup args
    host_template_id = 10

    # Mock logger
    logger.info.return_value = None

    # Mock _delete
    _delete.return_value = {host_template_id: True}

    # Call test function
    result = await delete_host_templates([host_template_id])

    # Assert _delete called with right args
    _delete.assert_awaited_once_with(HostTemplate, [host_template_id])

    # Assert result
    assert result == {host_template_id: True}
