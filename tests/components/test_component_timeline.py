import json
from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.timeline import get_host_timeline, get_service_timeline
from centreon_mcp.types.monitoring.timeline import TimelineFilter, TimelineOrder

MODULE = "centreon_mcp.components.timeline"


@patch(f"{MODULE}.TimelineEvent.list_for_host", new_callable=AsyncMock)
@patch(f"{MODULE}.TimelineFilter.join", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_get_host_timeline(
    logger: MagicMock, join: MagicMock, timeline_list_for_host: AsyncMock
):

    # Setup args
    host_id = 10
    filters = [TimelineFilter.model_construct()]
    limit = 50
    page = 1
    order = TimelineOrder.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock TimelineFilter.join
    conditions: dict = {}
    join.return_value = conditions

    # Mock TimelineEvent.list_for_host
    timeline_list_for_host.return_value = []

    # Call test function
    events = await get_host_timeline(host_id, filters, limit, page, order)

    # Assert TimelineEvent.list_for_host called with right args
    timeline_list_for_host.assert_awaited_once_with(
        host_id,
        search=json.dumps(conditions),
        limit=limit,
        page=page,
        sort_by=order.model_dump_json(exclude={"model_type"}),
    )

    # Asser result
    assert events == []


@patch(f"{MODULE}.TimelineEvent.list_for_service", new_callable=AsyncMock)
@patch(f"{MODULE}.TimelineFilter.join", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_get_service_timeline(
    logger: MagicMock, join: MagicMock, timeline_list_for_service: AsyncMock
):

    # Setup args
    host_id = 10
    service_id = 10
    filters = [TimelineFilter.model_construct()]
    limit = 50
    page = 1
    order = TimelineOrder.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock TimelineFilter.join
    conditions: dict = {}
    join.return_value = conditions

    # Mock TimelineEvent.list_for_service
    timeline_list_for_service.return_value = []

    # Call test function
    events = await get_service_timeline(host_id, service_id, filters, limit, page, order)

    # Assert TimelineEvent.list_for_service called with right args
    (
        timeline_list_for_service.assert_awaited_once_with(
            host_id,
            service_id,
            search=json.dumps(conditions),
            limit=limit,
            page=page,
            sort_by=order.model_dump_json(exclude={"model_type"}),
        )
    )

    # Assert result
    assert events == []
