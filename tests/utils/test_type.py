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
    Metric,
    PerformanceData,
    Resource,
    Service,
    ServiceStatusCount,
    StatusCount,
    TopMetricResult,
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


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_metric_list(request: AsyncMock):

    # Setup args
    host_id = 12
    service_id = 5

    # Mock request
    content = [
        {
            "id": 1,
            "name": "rta",
            "unit": "ms",
            "current_value": 0.025,
            "warning_high_threshold": 200.0,
            "warning_low_threshold": None,
            "critical_high_threshold": 400.0,
            "critical_low_threshold": None,
        },
        {
            "id": 2,
            "name": "pl",
            "unit": "%",
            "current_value": 0.0,
            "warning_high_threshold": 20.0,
            "warning_low_threshold": None,
            "critical_high_threshold": 50.0,
            "critical_low_threshold": None,
        },
    ]
    request.return_value = content

    # Call test function
    result = await Metric.list(host_id, service_id)

    # Assert request called with right args
    endpoint = f"monitoring/hosts/{host_id}/services/{service_id}/metrics"
    request.assert_awaited_once_with("GET", endpoint)

    # Assert result
    assert len(result) == 2
    assert result[0].name == "rta"
    assert result[0].unit == "ms"
    assert result[0].current_value == 0.025
    assert result[1].name == "pl"
    assert result[1].critical_high_threshold == 50.0


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_performance_data_get(request: AsyncMock):

    # Setup args
    host_id = 12
    service_id = 5
    start = "2024-01-15T08:00:00Z"
    end = "2024-01-15T20:00:00Z"

    # Mock request
    content = {
        "base": 1024,
        "metrics": [
            {
                "metric_id": 1,
                "metric": "used",
                "unit": "B",
                "legend": "used",
                "data": [1073741824.0, 1174405120.0, 1275068416.0],
                "warning_high_threshold": 2147483648.0,
                "warning_low_threshold": None,
                "critical_high_threshold": 3221225472.0,
                "critical_low_threshold": None,
            }
        ],
        "times": ["1705305600", "1705309200", "1705312800"],
    }
    request.return_value = content

    # Call test function
    result = await PerformanceData.get(host_id, service_id, start, end)

    # Assert request called with right args
    endpoint = f"monitoring/hosts/{host_id}/services/{service_id}/metrics/performance"
    request.assert_awaited_once_with("GET", endpoint, params={"start": start, "end": end})

    # Assert result
    assert result.base == 1024
    assert len(result.metrics) == 1
    assert result.metrics[0].metric == "used"
    assert result.metrics[0].unit == "B"
    assert len(result.metrics[0].data) == 3
    assert result.metrics[0].data[0] == 1073741824.0
    assert result.metrics[0].warning_high_threshold == 2147483648.0
    assert len(result.times) == 3


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_performance_data_get_defaults(request: AsyncMock):

    # Setup args
    host_id = 12
    service_id = 5

    # Mock request
    content = {"base": 1000, "metrics": [], "times": []}
    request.return_value = content

    # Call test function (no start/end, should default)
    result = await PerformanceData.get(host_id, service_id)

    # Assert request called with None params (filtered by request util)
    endpoint = f"monitoring/hosts/{host_id}/services/{service_id}/metrics/performance"
    request.assert_awaited_once_with("GET", endpoint, params={"start": None, "end": None})

    # Assert result
    assert result.base == 1000
    assert result.metrics == []
    assert result.times == []


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_top_metric_result_get(request: AsyncMock):

    # Setup args
    metric_name = "cpu"

    # Mock request
    content = {
        "name": "cpu",
        "unit": "%",
        "sort": "top",
        "limit": 10,
        "resources": [
            {
                "host_id": 14,
                "host_name": "db-prod-01",
                "service_id": 42,
                "service_display_name": "CPU",
                "current_value": 95.2,
            },
            {
                "host_id": 23,
                "host_name": "web-prod-03",
                "service_id": 55,
                "service_display_name": "CPU",
                "current_value": 87.1,
            },
        ],
    }
    request.return_value = content

    # Call test function
    result = await TopMetricResult.get(metric_name)

    # Assert request called with right args
    request.assert_awaited_once_with(
        "GET", "monitoring/dashboard/metrics/top", params={"metric_name": metric_name}
    )

    # Assert result
    assert result.name == "cpu"
    assert result.unit == "%"
    assert result.sort == "top"
    assert len(result.resources) == 2
    assert result.resources[0].host_name == "db-prod-01"
    assert result.resources[0].current_value == 95.2
    assert result.resources[1].service_display_name == "CPU"
