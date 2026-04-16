import json
from typing import List
from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.resource import (
    ResourceFilter,
    ResourceOrder,
    list_resources,
)
from centreon_mcp.utils.type import Resource, ResourceStatus, ResourceType, StatusType

MODULE = "centreon_mcp.components.resource"


@patch(f"{MODULE}.Resource.list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_resources(logger: MagicMock, list: AsyncMock):

    # Setup args
    filters = [ResourceFilter.model_construct()]
    types: List[ResourceType] = ["host", "service"]
    statuses: List[ResourceStatus] = ["UP", "WARNING"]
    hostgroup_names = ["hostgroup_name"]
    servicegroup_names = ["servicegroup_name"]
    host_category_names = ["host_category_name"]
    service_category_names = ["service_category_name"]
    monitoring_server_names = ["monitoring_server_name"]
    status_types: List[StatusType] = ["hard"]
    limit = 50
    page = 1
    order = ResourceOrder()

    # Mock logger
    logger.debug.return_value = None

    # Mock request
    resource = Resource.model_construct()
    list.return_value = [resource]

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
    conditions = (
        {
            "$or": [
                {"$and": filter.conditions} for filter in filters if filter.conditions
            ]
        }
        if filters
        else {}
    )
    sort_by = order.model_dump_json()
    list.assert_awaited_once_with(
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
