import json
from unittest.mock import AsyncMock, call, patch

import pytest
from pydantic import BaseModel

from centreon_mcp.components.base import (
    _create,
    _delete,
    _list,
    _update,
)
from centreon_mcp.types.base import BaseFilter, BaseOrder
from centreon_mcp.types.configuration.command import Command
from centreon_mcp.types.configuration.host import HostConfiguration, HostConfigurationPartialParams
from centreon_mcp.types.configuration.host_category import (
    HostCategoryConfiguration,
    HostCategoryConfigurationFullParams,
    HostCategoryConfigurationPartialParams,
)
from centreon_mcp.types.configuration.host_group import (
    HostGroupConfiguration,
    HostGroupConfigurationFullParams,
    HostGroupConfigurationPartialParams,
)
from centreon_mcp.types.configuration.host_severity import (
    HostSeverity,
    HostSeverityFullParams,
    HostSeverityPartialParams,
)
from centreon_mcp.types.configuration.host_template import (
    HostTemplate,
    HostTemplateFullParams,
    HostTemplatePartialParams,
)
from centreon_mcp.types.configuration.monitoring_server import MonitoringServerConfiguration
from centreon_mcp.types.monitoring.acknowledgement import Acknowledgement
from centreon_mcp.types.monitoring.downtime import Downtime
from centreon_mcp.types.monitoring.monitoring_server import MonitoringServer
from centreon_mcp.types.monitoring.resource import Resource
from centreon_mcp.types.monitoring.servicegroup import ServiceGroup
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, UpdateMixin
from centreon_mcp.utils.request import CentreonAPIError

MODULE = "centreon_mcp.components.base"


@pytest.mark.parametrize(
    "model,params",
    [
        (HostCategoryConfiguration, HostCategoryConfigurationFullParams.model_construct()),
        (HostGroupConfiguration, HostGroupConfigurationFullParams.model_construct()),
        (HostSeverity, HostSeverityFullParams.model_construct()),
        (HostTemplate, HostTemplateFullParams.model_construct()),
    ],
)
@patch(f"{MODULE}.CreateMixin.create", new_callable=AsyncMock)
async def test_create(create_mixin: AsyncMock, model: type[CreateMixin], params: BaseModel):

    # CreateMixin.create
    create_mixin.return_value = True

    # Call test function
    result = await _create(model, params)

    # Assert CreateMixin.create called with right args
    create_mixin.assert_awaited_once_with(params)

    # Assert result
    assert result


@pytest.mark.parametrize(
    "model",
    [
        HostConfiguration,
        HostGroupConfiguration,
        HostCategoryConfiguration,
        HostSeverity,
        Downtime,
        HostTemplate,
    ],
)
@patch(f"{MODULE}.DeleteMixin.delete", new_callable=AsyncMock)
async def test_delete(delete_mixin: AsyncMock, model: type[DeleteMixin]):

    # Setup args
    model_ids = [1, 2]

    # Mock DeleteMixin.delete
    error = CentreonAPIError(404, "fake_url", "GET", {})
    delete_mixin.side_effect = [True, error]

    # Call test function
    results = await _delete(model, model_ids)

    # Assert DeleteMixin.delete called with right args
    delete_mixin.assert_has_awaits([call(model_id) for model_id in model_ids])

    # Assert result
    assert results == {model_ids[0]: True, model_ids[1]: error}


@pytest.mark.parametrize(
    "model, instance",
    [
        (Acknowledgement, Acknowledgement.model_construct()),
        (Command, Command.model_construct()),
        (HostConfiguration, HostConfiguration.model_construct()),
        (HostGroupConfiguration, HostGroupConfiguration.model_construct()),
        (HostCategoryConfiguration, HostCategoryConfiguration.model_construct()),
        (HostSeverity, HostSeverity.model_construct()),
        (Downtime, Downtime.model_construct()),
        (HostTemplate, HostTemplate.model_construct()),
        (MonitoringServer, MonitoringServer.model_construct()),
        (ServiceGroup, ServiceGroup.model_construct()),
        (Resource, Resource.model_construct()),
        (MonitoringServerConfiguration, MonitoringServerConfiguration.model_construct()),
    ],
)
@patch(f"{MODULE}.ListMixin.list", new_callable=AsyncMock)
async def test_list(list_mixin: AsyncMock, model: type[ListMixin], instance: ListMixin):

    # Setup args
    filters = [BaseFilter()]
    limit = 10
    page = 1
    order = BaseOrder()
    extras = None

    # Mock ListMixin.list
    list_mixin.return_value = [instance]

    # Call test function
    results = await _list(model, filters, limit, page, order, extras)

    # Assert ListMixin.list called with right args
    search = json.dumps(BaseFilter.join(filters))
    sort_by = order.model_dump_json(exclude={"model_type"})
    list_mixin.assert_awaited_once_with(search, limit, page, sort_by, extras)

    # Assert result
    assert results == [instance]


@pytest.mark.parametrize(
    "model_cls,partial_params",
    [
        (HostConfiguration, HostConfigurationPartialParams.model_construct()),
        (HostTemplate, HostTemplatePartialParams.model_construct()),
        (
            HostGroupConfiguration,
            HostGroupConfigurationPartialParams.model_construct(name="host_group_name"),
        ),
        (
            HostCategoryConfiguration,
            HostCategoryConfigurationPartialParams.model_construct(
                name="host_category_name", alias="host_category_alias"
            ),
        ),
        (
            HostSeverity,
            HostSeverityPartialParams.model_construct(
                name="host_severity_name", alias="host_severity_alias", level=1, icon_id=1
            ),
        ),
    ],
)
async def test_update(
    model_cls: type[UpdateMixin],
    partial_params: BaseModel,
):
    # Setup args
    model_id = 10

    # Call test function
    with patch.object(model_cls, "update", new_callable=AsyncMock) as update_mixin:
        # Mock UpdateMixin.update
        update_mixin.return_value = True

        result = await _update(model_cls, model_id, partial_params)

    # Assert UpdateMixin.update called with right args
    update_mixin.assert_awaited_once_with(model_id, partial_params)

    # Assert result
    assert result
