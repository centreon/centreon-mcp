from datetime import datetime
from unittest.mock import AsyncMock, patch

from centreon_mcp.utils.type import (
    Acknowledgement,
    AcknowledgementParams,
    AcknowledgementResource,
    Comment,
    CommentResource,
    Downtime,
    DowntimeParams,
    DowntimeResource,
    Resource,
)

MODULE = "centreon_mcp.utils.type"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_list_resources(request: AsyncMock):

    # Setup args
    search = ""
    types = ""
    statuses = ""
    hostgroup_names = ""
    servicegroup_names = ""
    host_category_names = ""
    service_category_names = ""
    monitoring_server_names = ""
    status_types = ""
    limit = 1
    page = 1
    sort_by = ""

    # Mock request
    content: dict = {"result": []}
    request.return_value = content

    # Call test function
    result = await Resource.list(
        search,
        types,
        statuses,
        hostgroup_names,
        servicegroup_names,
        host_category_names,
        service_category_names,
        monitoring_server_names,
        status_types,
        limit,
        page,
        sort_by,
    )

    # Assert request called with right args
    params = {
        "search": search,
        "limit": limit,
        "page": page,
        "sort_by": sort_by,
        "types": types,
        "statuses": statuses,
        "hostgroup_names": hostgroup_names,
        "servicegroup_names": servicegroup_names,
        "host_category_names": host_category_names,
        "service_category_names": service_category_names,
        "monitoring_server_names": monitoring_server_names,
        "status_types": status_types,
    }
    request.assert_awaited_once_with("GET", Resource.endpoint, params=params)

    # Assert result
    assert len(result) == 0


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_add_acknowledgement(request: AsyncMock):

    # Setup args
    params = AcknowledgementParams(comment="Comment")
    resources = [AcknowledgementResource(type="host", resource_id=10, host_id=10)]

    # Mock request
    request.return_value = None

    # Call test function
    await Acknowledgement.add(params, resources)

    # Assert request called with right args
    payload = {
        "acknowledgement": params.model_dump(mode="json"),
        "resources": [resource.dump() for resource in resources],
    }
    request.assert_awaited_once_with(
        "POST", "monitoring/resources/acknowledge", payload=payload
    )


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_cancel_acknowledgement(request: AsyncMock):

    # Setup args
    with_services = True
    resources = [AcknowledgementResource(type="host", resource_id=10, host_id=10)]

    # Mock request
    request.return_value = None

    # Call test function
    await Acknowledgement.cancel(True, resources)

    # Assert request called with right args
    payload = {
        "disacknowledgement": {"with_services": with_services},
        "resources": [resource.dump() for resource in resources],
    }
    request.assert_awaited_once_with(
        "DELETE", "monitoring/resources/acknowledgements", payload=payload
    )


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_set_downtime(request: AsyncMock):

    # Setup args
    params = DowntimeParams(
        start_time=datetime(2026, 4, 1),
        end_time=datetime(2026, 4, 30),
        is_fixed=True,
        duration=1,
        comment="Comment",
        with_services=True,
    )
    resources = [DowntimeResource(type="host", resource_id=10, host_id=10)]

    # Mock request
    request.return_value = None

    # Call test function
    await Downtime.set(params, resources)

    # Assert request called with right args
    payload = {
        "downtime": params.model_dump(mode="json"),
        "resources": [resource.dump() for resource in resources],
    }
    request.assert_awaited_once_with(
        "POST", "monitoring/resources/downtime", payload=payload
    )


@staticmethod
@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_cancel_downtime(request: AsyncMock):

    # Setup args
    downtime_id = 10

    # Mock request
    request.return_value = None

    # Call test function
    await Downtime.cancel(downtime_id)

    # Assert request called with right args
    request.assert_awaited_once_with("DELETE", f"monitoring/downtimes/{downtime_id}")


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_add_comment(request: AsyncMock):

    # Setup args
    resources = [
        CommentResource(
            type="host",
            resource_id=10,
            host_id=10,
            comment="Comment",
            date=datetime(2026, 4, 7),
        )
    ]

    # Mock request
    request.return_value = None

    # Call test function
    await Comment.add(resources)

    # Assert request called with right args
    payload = {"resources": [resource.dump() for resource in resources]}
    request.assert_awaited_once_with(
        "POST", "monitoring/resources/comments", payload=payload
    )
