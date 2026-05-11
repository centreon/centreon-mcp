from unittest.mock import AsyncMock, patch

from centreon_mcp.types.resource import Resource

MODULE = "centreon_mcp.types.resource"


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
