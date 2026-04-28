from unittest.mock import AsyncMock, patch

from centreon_mcp.utils.type import (
    Acknowledgement,
    AcknowledgementParams,
    AcknowledgementResource,
    Command,
    CommandParams,
    Comment,
    CommentResource,
    Downtime,
    DowntimeParams,
    DowntimeResource,
    Host,
    HostStatusCount,
    Resource,
    Service,
    ServiceStatusCount,
    StatusCount,
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
async def test_host_count_by_status(request: AsyncMock):

    # Setup args
    search = ""

    # Mock request
    content: dict = {
        "up": {"total": 10},
        "down": {"total": 10},
        "unreachable": {"total": 10},
        "pending": {"total": 10},
        "total": 40,
    }
    request.return_value = content

    # Call test function
    result = await Host.count_by_status(search)

    # Assert request called with right args
    params = {"search": search}
    request.assert_awaited_once_with("GET", "monitoring/hosts/status", params=params)

    # Assert result
    assert result == HostStatusCount(**content)


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_service_count_by_status(request: AsyncMock):

    # Setup args
    search = ""

    # Mock request
    content: dict = {
        "ok": {"total": 10},
        "warning": {"total": 10},
        "critical": {"total": 10},
        "unknown": {"total": 10},
        "pending": {"total": 10},
        "total": 50,
    }
    request.return_value = content

    # Call test function
    result = await Service.count_by_status(search)

    # Assert request called with right args
    params = {"search": search}
    request.assert_awaited_once_with("GET", "monitoring/services/status", params=params)

    # Assert result
    assert result == ServiceStatusCount(**content)


async def test_status_count_flatten():

    # Setup args
    data: dict = {
        "ok": {"total": 10},
        "warning": {"total": 10},
        "critical": {"total": 10},
        "unknown": {"total": 10},
        "pending": {"total": 10},
        "total": 50,
    }

    # Call test function
    result = StatusCount.flatten(data)

    # Assert result
    assert result == {
        "ok": 10,
        "warning": 10,
        "critical": 10,
        "unknown": 10,
        "pending": 10,
        "total": 50,
    }


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_add_acknowledgement(request: AsyncMock):

    # Setup args
    params = AcknowledgementParams.model_construct()
    resources = [AcknowledgementResource.model_construct(host_id=10)]

    # Mock request
    request.return_value = None

    # Call test function
    await Acknowledgement.add(params, resources)

    # Assert request called with right args
    payload = {
        "acknowledgement": params.model_dump(mode="json"),
        "resources": [resource.dump() for resource in resources],
    }
    request.assert_awaited_once_with("POST", "monitoring/resources/acknowledge", payload=payload)


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_cancel_acknowledgement(request: AsyncMock):

    # Setup args
    with_services = True
    resources = [AcknowledgementResource.model_construct(host_id=10)]

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
    params = DowntimeParams.model_construct()
    resources = [DowntimeResource.model_construct(host_id=10)]

    # Mock request
    request.return_value = None

    # Call test function
    await Downtime.set(params, resources)

    # Assert request called with right args
    payload = {
        "downtime": params.model_dump(mode="json"),
        "resources": [resource.dump() for resource in resources],
    }
    request.assert_awaited_once_with("POST", "monitoring/resources/downtime", payload=payload)


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
    resources = [CommentResource.model_construct(host_id=10)]

    # Mock request
    request.return_value = None

    # Call test function
    await Comment.add(resources)

    # Assert request called with right args
    payload = {"resources": [resource.dump() for resource in resources]}
    request.assert_awaited_once_with("POST", "monitoring/resources/comments", payload=payload)


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_add_command(request: AsyncMock):

    # Setup args
    params = CommandParams.model_construct()

    # Mock request
    request.return_value = None

    # Call test function
    await Command.add(params)

    # Assert request called with right args
    payload = params.model_dump(mode="json")
    request.assert_awaited_once_with("POST", "configuration/commands", payload=payload)
