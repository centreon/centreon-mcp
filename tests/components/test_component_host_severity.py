from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.host_severity import (
    HostSeverityFilter,
    HostSeverityOrder,
    create_host_severity,
    delete_host_severities,
    list_host_severities,
)
from centreon_mcp.types.host_severity import HostSeverity, HostSeverityParams

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

    # Call test fonction
    results = await list_host_severities(filters, limit, page, order)

    # Assert _list called with right args
    _list.assert_awaited_once_with(HostSeverity, HostSeverityOrder, filters, limit, page, order)

    # Assert result
    assert results[0] == host_severity


@patch(f"{MODULE}.HostSeverity.create", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_create_host_severity(logger: MagicMock, host_severity_create: AsyncMock):

    # Setup args
    params = HostSeverityParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock HostSeverity.create
    host_severity_create.return_value = None

    # Call test fonction
    result = await create_host_severity(params)

    # Assert HostSeverity.create called with right args
    host_severity_create.assert_awaited_once_with(params)

    # Assert result
    assert result


@patch(f"{MODULE}.HostSeverity.delete", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_delete_host_severity(logger: MagicMock, host_severity_delete: AsyncMock):

    # Setup args
    host_severity_id = 10

    # Mock logger
    logger.info.return_value = None

    # Mock HostSeverity.delete
    host_severity_delete.return_value = None

    # Call test fonction
    result = await delete_host_severities([host_severity_id])

    # Assert HostSeverity.delete called with right args
    host_severity_delete.assert_awaited_once_with(host_severity_id)

    # Assert result
    assert result
