import json
from unittest.mock import AsyncMock, patch

import pytest
from pydantic import BaseModel

from centreon_mcp.components.base import BaseFilter, BaseOrder, _create, _delete, _list
from centreon_mcp.types.acknowledgement import Acknowledgement
from centreon_mcp.types.command import Command
from centreon_mcp.types.downtime import Downtime
from centreon_mcp.types.host import HostConfiguration
from centreon_mcp.types.host_category import (
    HostCategoryConfiguration,
    HostCategoryConfigurationFullParams,
)
from centreon_mcp.types.host_group import HostGroupConfiguration, HostGroupConfigurationFullParams
from centreon_mcp.types.host_severity import HostSeverity, HostSeverityFullParams
from centreon_mcp.types.host_template import HostTemplate, HostTemplateFullParams
from centreon_mcp.types.monitoring_server import MonitoringServer
from centreon_mcp.types.servicegroup import ServiceGroup
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin

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
async def test_create[CentreonModel: CreateMixin](
    create_mixin: AsyncMock, model: type[CentreonModel], params: BaseModel
):

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
async def test_delete[CentreonModel: DeleteMixin](
    delete_mixin: AsyncMock, model: type[CentreonModel]
):

    # Setup args
    model_id = 1

    # Mock DeleteMixin.delete
    delete_mixin.return_value = True

    # Call test function
    results = await _delete(model, [model_id])

    # Assert DeleteMixin.delete called with right args
    delete_mixin.assert_awaited_once_with(model_id)

    # Assert result
    assert results == {model_id: True}


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
    ],
)
@patch(f"{MODULE}.ListMixin.list", new_callable=AsyncMock)
async def test_list[CentreonModel: ListMixin](
    list_mixin: AsyncMock, model: type[CentreonModel], instance: CentreonModel
):

    # Setup args
    filters = [BaseFilter()]
    limit = 10
    page = 1
    order = BaseOrder()

    # Mock ListMixin.list
    list_mixin.return_value = [instance]

    # Call test function
    results = await _list(model, filters, limit, page, order)

    # Assert ListMixin.list called with right args
    search = json.dumps(BaseFilter.join(filters))
    sort_by = order.model_dump_json()
    list_mixin.assert_awaited_once_with(search, limit, page, sort_by)

    # Assert result
    assert results == [instance]
