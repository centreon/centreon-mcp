from unittest.mock import AsyncMock, patch

from centreon_mcp.types.timeline import TimelineEvent

MODULE = "centreon_mcp.types.timeline"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_timeline_list_for_host(request: AsyncMock):

    # Setup args
    host_id = 10
    search = ""
    limit = 50
    page = 1
    sort_by = ""

    # Mock request
    request.return_value = {"result": []}

    # Call test function
    events = await TimelineEvent.list_for_host(host_id, search, limit, page, sort_by)

    # Assert request called with right args
    params = {"search": search, "limit": limit, "page": page, "sort_by": sort_by}
    request.assert_awaited_once_with("GET", f"monitoring/hosts/{host_id}/timeline", params=params)

    # Assert results
    assert events == []


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_timeline_list_for_service(request: AsyncMock):

    # Setup args
    host_id = 10
    service_id = 10
    limit = 50
    page = 1
    search = ""
    sort_by = ""

    # Mock request
    request.return_value = {"result": []}

    # Call test function
    events = await TimelineEvent.list_for_service(host_id, service_id, search, limit, page, sort_by)

    # Assert request called with right args
    params = {"search": search, "limit": 50, "page": 1, "sort_by": ""}
    request.assert_awaited_once_with(
        "GET", f"monitoring/hosts/{host_id}/services/{service_id}/timeline", params=params
    )

    # Assert results
    assert events == []
