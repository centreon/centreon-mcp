import json
from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.resource import (
    ResourceFilter,
    ResourceOrder,
    TimelineFilter,
    TimelineOrder,
    get_resource_timeline,
    list_resources,
)
from centreon_mcp.utils.type import (
    Resource,
    ResourceStatus,
    ResourceType,
    StatusType,
    TimelineResource,
)

MODULE = "centreon_mcp.components.resource"


@patch(f"{MODULE}.Resource.list", new_callable=AsyncMock)
@patch(f"{MODULE}.ResourceFilter.join", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_resources(logger: MagicMock, join: MagicMock, resource_list: AsyncMock):

    # Setup args
    filters = [ResourceFilter.model_construct()]
    types: list[ResourceType] = ["host", "service"]
    statuses: list[ResourceStatus] = ["UP", "WARNING"]
    hostgroup_names = ["hostgroup_name"]
    servicegroup_names = ["servicegroup_name"]
    host_category_names = ["host_category_name"]
    service_category_names = ["service_category_name"]
    monitoring_server_names = ["monitoring_server_name"]
    status_types: list[StatusType] = ["hard"]
    limit = 50
    page = 1
    order = ResourceOrder()

    # Mock logger
    logger.debug.return_value = None

    # Mock ResourceFilter.join
    conditions: dict = {}
    join.return_value = conditions

    # Mock request
    resource = Resource.model_construct()
    resource_list.return_value = [resource]

    # Call test fonction
    results = await list_resources(
        filters,
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
        order,
    )

    # Assert request called with right args
    sort_by = order.model_dump_json()
    resource_list.assert_awaited_once_with(
        search=json.dumps(conditions),
        types=json.dumps(types or []),
        statuses=json.dumps(statuses or []),
        hostgroup_names=json.dumps(hostgroup_names or []),
        servicegroup_names=json.dumps(servicegroup_names or []),
        host_category_names=json.dumps(host_category_names or []),
        service_category_names=json.dumps(service_category_names or []),
        monitoring_server_names=json.dumps(monitoring_server_names or []),
        status_types=json.dumps(status_types or []),
        limit=limit,
        page=page,
        sort_by=sort_by,
    )

    # Assert result
    assert results[0] == resource


@patch(f"{MODULE}.TimelineEvent.list_for", new_callable=AsyncMock)
@patch(f"{MODULE}.TimelineFilter.join", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_get_resource_timeline_default_order(
    logger: MagicMock, join: MagicMock, list_for: AsyncMock
):

    # Setup args
    resource = TimelineResource(type="host", host_id=11)
    filters = [TimelineFilter.model_construct()]
    limit = 50
    page = 1

    # Mock logger
    logger.info.return_value = None

    # Mock TimelineFilter.join
    conditions: dict = {}
    join.return_value = conditions

    # Mock TimelineEvent.list_for
    list_for.return_value = []

    # Call test function (no order, should default to date DESC)
    await get_resource_timeline(resource, filters, limit, page, None)

    # Assert TimelineEvent.list_for called with right args
    expected_sort_by = TimelineOrder().model_dump_json()
    list_for.assert_awaited_once_with(
        resource=resource,
        search=json.dumps(conditions),
        limit=limit,
        page=page,
        sort_by=expected_sort_by,
    )

    # Verify default order is date DESC (most recent first)
    assert '"field":"date"' in expected_sort_by
    assert '"order":"DESC"' in expected_sort_by


@patch(f"{MODULE}.TimelineEvent.list_for", new_callable=AsyncMock)
@patch(f"{MODULE}.TimelineFilter.join", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_get_resource_timeline_explicit_order(
    logger: MagicMock, join: MagicMock, list_for: AsyncMock
):

    # Setup args
    resource = TimelineResource(type="service", host_id=11, service_id=42)
    filters = [TimelineFilter.model_construct()]
    order = TimelineOrder(field="type", order="ASC")

    # Mocks
    logger.info.return_value = None
    join.return_value = {}
    list_for.return_value = []

    # Call
    await get_resource_timeline(resource, filters, 50, 1, order)

    # Assert sort_by reflects the explicit order
    list_for.assert_awaited_once_with(
        resource=resource,
        search=json.dumps({}),
        limit=50,
        page=1,
        sort_by=order.model_dump_json(),
    )
