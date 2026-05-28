from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.host_template import (
    HostTemplateFilter,
    HostTemplateOrder,
    create_host_template,
    delete_host_templates,
    list_host_templates,
    update_host_template,
)
from centreon_mcp.types.host_template import (
    HostTemplate,
    HostTemplateFullParams,
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

    # Call test fonction
    results = await list_host_templates(filters, limit, page, order)

    # Assert _list called with right args
    _list.assert_awaited_once_with(HostTemplate, HostTemplateOrder, filters, limit, page, order)

    # Assert result
    assert results[0] == host_template


@patch(f"{MODULE}.HostTemplate.create", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_create_host_template(logger: MagicMock, host_template_create: AsyncMock):

    # Setup args
    params = HostTemplateFullParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock HostTemplate.create
    host_template_create.return_value = True

    # Call test fonction
    result = await create_host_template(params)

    # Assert HostTemplate.create called with right args
    host_template_create.assert_awaited_once_with(params)

    # Assert result
    assert result


@patch(f"{MODULE}.HostTemplate.patch", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_update_host_template(logger: MagicMock, host_template_patch: AsyncMock):

    # Setup args
    host_id = 10
    params = HostTemplatePartialParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock HostTemplate.patch
    host_template_patch.return_value = True

    # Call test fonction
    result = await update_host_template(host_id, params)

    # Assert HostTemplate.patch called with right args
    host_template_patch.assert_awaited_once_with(host_id, params)

    # Assert result
    assert result


@patch(f"{MODULE}.HostTemplate.delete", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_delete_host_templates(logger: MagicMock, host_template_delete: AsyncMock):

    # Setup args
    host_template_id = 10

    # Mock logger
    logger.info.return_value = None

    # Mock HostTemplate.delete
    host_template_delete.return_value = True

    # Call test fonction
    result = await delete_host_templates([host_template_id])

    # Assert HostTemplate.delete called with right args
    host_template_delete.assert_awaited_once_with(host_template_id)

    # Assert result
    assert result == {host_template_id: True}
