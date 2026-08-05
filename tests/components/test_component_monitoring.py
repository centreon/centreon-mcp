import json
from typing import Literal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from centreon_mcp.components.monitoring import (
    cancel_monitoring_actions,
    count_monitoring_resources_by_status,
    list_monitoring_actions,
    list_monitoring_entities,
    list_monitoring_resources,
    set_monitoring_actions,
)
from centreon_mcp.types.monitoring.mapping import MODELS_MIXIN_SET
from centreon_mcp.types.monitoring.resource import Resource, ResourceFilter, ResourceOrder
from centreon_mcp.utils.base import BaseResource

MODULE = "centreon_mcp.components.monitoring"


@patch(f"{MODULE}.Resource.list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_monitoring_resources(logger: MagicMock, list_mixin: AsyncMock):

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
    list_mixin.return_value = [resource]

    # Call test function
    results = await list_monitoring_resources(
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
    list_mixin.assert_awaited_once_with(filters, limit, page, order, extras)

    # Assert result
    assert results[0] == resource


@pytest.mark.parametrize(
    "model_type",
    [
        "host_group",
        "service_group",
        "monitoring_server",
    ],
)
@patch("centreon_mcp.utils.mixins.ListMixin.list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_monitoring_entities(
    logger: MagicMock,
    list_mixin: AsyncMock,
    model_type: Literal[
        "host_group",
        "service_group",
        "monitoring_server",
    ],
):

    # Setup args
    filters = [MagicMock()]
    limit = 50
    page = 1
    order = MagicMock()

    # Mock logger
    logger.debug.return_value = None

    model = MagicMock()
    list_mixin.return_value = [model]

    # Call test function
    results = await list_monitoring_entities(model_type, filters, limit, page, order)

    # Assert ListMixin.list called with right args
    list_mixin.assert_awaited_once_with(filters, limit, page, order)

    # Assert result
    assert results == [model]


@pytest.mark.parametrize(
    "model_type",
    ["acknowledgement", "downtime"],
)
@patch("centreon_mcp.utils.mixins.ListMixin.list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_monitoring_actions(
    logger: MagicMock,
    list_mixin: AsyncMock,
    model_type: Literal["acknowledgement", "downtime"],
):

    # Setup args
    filters = [MagicMock()]
    limit = 50
    page = 1
    order = MagicMock()

    # Mock logger
    logger.debug.return_value = None

    model = MagicMock()
    list_mixin.return_value = [model]

    # Call test function
    results = await list_monitoring_actions(model_type, filters, limit, page, order)

    # Assert ListMixin.list called with right args
    list_mixin.assert_awaited_once_with(filters, limit, page, order)

    # Assert result
    assert results == [model]


@pytest.mark.parametrize(
    "model_type",
    ["acknowledgement", "downtime", "comment", "check"],
)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_set_monitoring_action(
    logger: MagicMock,
    model_type: Literal["acknowledgement", "downtime", "comment", "check"],
):

    # Setup args
    params = MagicMock()
    resources = [BaseResource(type="host", resource_id=10, host_id=10)]

    # Mock logger
    logger.info.return_value = None

    model_class = MODELS_MIXIN_SET[model_type]
    path = f"{model_class.__module__}.{model_class.__qualname__}.set"

    with patch(path, new_callable=AsyncMock) as set_mixin:
        # Mock SetMixin.set
        set_mixin.return_value = True

        # Call test function
        result = await set_monitoring_actions(model_type, params, resources)

        # Assert SetMixin.set called with right args
        set_mixin.assert_awaited_once_with(params, resources)

    # Assert result
    assert result


@pytest.mark.parametrize(
    "model_type",
    ["acknowledgement", "downtime"],
)
@patch("centreon_mcp.utils.mixins.DeleteMixin.delete", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_cancel_monitoring_actions(
    logger: MagicMock,
    delete: AsyncMock,
    model_type: Literal["acknowledgement", "downtime"],
):

    # Setup args
    model_id = 10

    # Mock logger
    logger.info.return_value = None

    # Mock DeleteMixin.delete
    delete.return_value = {model_id: True}

    # Call test function
    result = await cancel_monitoring_actions(model_type, [model_id])

    # Assert DeleteMixin.delete called with right args
    delete.assert_awaited_once_with([model_id])

    # Assert result
    assert result == {model_id: True}


@pytest.mark.parametrize(
    "model_type",
    ["host", "service"],
)
@patch("centreon_mcp.utils.mixins.CountMixin.count", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_count_monitoring_resource_by_status(
    logger: MagicMock,
    count_mixin: AsyncMock,
    model_type: Literal["host", "service"],
):

    # Setup args
    filters = [MagicMock()]

    # Mock logger
    logger.debug.return_value = None

    # Mock CountMixin.count
    count = MagicMock()
    count_mixin.return_value = count

    # Call test function
    result = await count_monitoring_resources_by_status(model_type, filters)

    # Assert CountMixin.count called with correct args
    count_mixin.assert_awaited_once_with(filters)

    # Assert result
    assert result == count
