from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.host_severity import (
    HostSeverityFilter,
    HostSeverityOrder,
    create_host_severity,
    delete_host_severities,
    list_host_severities,
    update_host_severity,
)
from centreon_mcp.types.host_severity import (
    HostSeverity,
    HostSeverityFullParams,
    HostSeverityPartialParams,
)

MODULE = "centreon_mcp.components.host_severity"


@patch(f"{MODULE}._list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_host_severities(logger: MagicMock, _list: AsyncMock):

    # Setup args
    filters = [HostSeverityFilter.model_construct()]
    limit = 50
    page = 1
    order = HostSeverityOrder.model_construct()

    # Mock logger
    logger.debug.return_value = None

    # Mock _list
    host_severity = HostSeverity.model_construct()
    _list.return_value = [host_severity]

    # Call test function
    results = await list_host_severities(filters, limit, page, order)

    # Assert _list called with right args
    _list.assert_awaited_once_with(HostSeverity, filters, limit, page, order)

    # Assert result
    assert results[0] == host_severity


@patch(f"{MODULE}._create", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_create_host_severity(logger: MagicMock, _create: AsyncMock):

    # Setup args
    params = HostSeverityFullParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock _create
    _create.return_value = True

    # Call test function
    result = await create_host_severity(params)

    # Assert _create called with right args
    _create.assert_awaited_once_with(HostSeverity, params)

    # Assert result
    assert result


@patch(f"{MODULE}._update", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_update_host_severity(logger: MagicMock, _update: AsyncMock):

    # Setup args
    host_severity_id = 10
    params = HostSeverityPartialParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock _update
    _update.return_value = True

    # Call test function
    result = await update_host_severity(host_severity_id, params)

    # Assert _update called with right args
    _update.assert_awaited_once_with(HostSeverity, HostSeverityFullParams, host_severity_id, params)

    # Assert result
    assert result


@patch(f"{MODULE}._delete", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_delete_host_severities(logger: MagicMock, _delete: AsyncMock):

    # Setup args
    host_severity_id = 10

    # Mock logger
    logger.info.return_value = None

    # Mock _delete
    _delete.return_value = {host_severity_id: True}

    # Call test function
    result = await delete_host_severities([host_severity_id])

    # Assert _delete called with right args
    _delete.assert_awaited_once_with(HostSeverity, [host_severity_id])

    # Assert result
    assert result == {host_severity_id: True}
