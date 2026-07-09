import json
from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.resource import list_resources
from centreon_mcp.types.monitoring.resource import Resource, ResourceFilter, ResourceOrder

MODULE = "centreon_mcp.components.resource"


@patch(f"{MODULE}.Resource.list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_resources(logger: MagicMock, list: AsyncMock):

    # Setup args
    filters = [ResourceFilter.model_construct()]
    limit = 50
    page = 1
    order = ResourceOrder()
    hostgroup_names = ["hostgroup_name_10"]
    monitoring_server_names = ["monitoring_server_name_10"]

    # Mock logger
    logger.info.return_value = None

    # Mock Resource.list
    resource = Resource.model_construct()
    list.return_value = [resource]

    # Call test function
    results = await list_resources(
        filters,
        limit=limit,
        page=page,
        order=order,
        hostgroup_names=hostgroup_names,
        monitoring_server_names=monitoring_server_names,
    )

    # Assert Resource.list called with right args
    fields = {
        "hostgroup_names": hostgroup_names,
        "monitoring_server_names": monitoring_server_names,
    }
    extras = {name: json.dumps(value) for name, value in fields.items() if value}
    list.assert_awaited_once_with(filters, limit, page, order, extras)

    # Assert result
    assert results[0] == resource
