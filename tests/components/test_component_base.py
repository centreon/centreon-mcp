import json
from unittest.mock import AsyncMock, call, patch

import pytest
from pydantic import BaseModel

from centreon_mcp.components.base import (
    BaseFilter,
    BaseOrder,
    _create,
    _delete,
    _list,
    _patch,
    _update,
)
from centreon_mcp.types.acknowledgement import Acknowledgement
from centreon_mcp.types.command import Command
from centreon_mcp.types.downtime import Downtime
from centreon_mcp.types.host import HostConfiguration, HostConfigurationPartialParams
from centreon_mcp.types.host_category import (
    HostCategoryConfiguration,
    HostCategoryConfigurationFullParams,
    HostCategoryConfigurationPartialParams,
)
from centreon_mcp.types.host_group import HostGroupConfiguration, HostGroupConfigurationFullParams
from centreon_mcp.types.host_severity import (
    HostSeverity,
    HostSeverityFullParams,
    HostSeverityPartialParams,
)
from centreon_mcp.types.host_template import (
    HostTemplate,
    HostTemplateFullParams,
    HostTemplatePartialParams,
)
from centreon_mcp.types.monitoring_server import MonitoringServer
from centreon_mcp.types.resource import Resource
from centreon_mcp.types.servicegroup import ServiceGroup
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, PatchMixin, UpdateMixin
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
    extras = None

    # Mock ListMixin.list
    list_mixin.return_value = [instance]

    # Call test function
    results = await _list(model, filters, limit, page, order, extras)

    # Assert ListMixin.list called with right args
    search = json.dumps(BaseFilter.join(filters))
    sort_by = order.model_dump_json()
    list_mixin.assert_awaited_once_with(search, limit, page, sort_by, extras)

    # Assert result
    assert results == [instance]


@pytest.mark.parametrize(
    "model,params",
    [
        (HostConfiguration, HostConfigurationPartialParams.model_construct()),
        (HostTemplate, HostTemplatePartialParams.model_construct()),
    ],
)
@patch(f"{MODULE}.PatchMixin.patch", new_callable=AsyncMock)
async def test_patch[CentreonModel: PatchMixin](
    patch_mixin: AsyncMock, model: type[CentreonModel], params: BaseModel
):
    # Setup args
    model_id = 10

    # Mock PatchMixin.patch
    patch_mixin.return_value = True

    # Call test function
    result = await _patch(model, model_id, params)

    # Assert PatchMixin.patch called with right args
    patch_mixin.assert_awaited_once_with(model_id, params)

    # Assert result
    assert result


@pytest.mark.parametrize(
    "model_cls,full_params_cls,partial_params",
    [
        (
            HostGroupConfiguration,
            HostGroupConfigurationFullParams,
            HostConfigurationPartialParams.model_construct(name="host_group_name"),
        ),
        (
            HostCategoryConfiguration,
            HostCategoryConfigurationFullParams,
            HostCategoryConfigurationPartialParams.model_construct(
                name="host_category_name", alias="host_category_alias"
            ),
        ),
        (
            HostSeverity,
            HostGroupConfigurationFullParams,
            HostSeverityPartialParams.model_construct(name="host_severity_name"),
        ),
    ],
)
@patch(f"{MODULE}.UpdateMixin.update", new_callable=AsyncMock)
@patch(f"{MODULE}.UpdateMixin.get", new_callable=AsyncMock)
async def test_update[CentreonModel: UpdateMixin](
    get_mixin: AsyncMock,
    update_mixin: AsyncMock,
    model_cls: type[CentreonModel],
    full_params_cls: type[BaseModel],
    partial_params: BaseModel,
):
    # Setup args
    model_id = 10

    # Mock ReadMixin.get
    model = model_cls.model_construct()  # type: ignore
    get_mixin.return_value = model

    # Mock UpdateMixin.update
    update_mixin.return_value = True

    # Call test function
    result = await _update(model_cls, full_params_cls, model_id, partial_params)

    # Assert ReadMixin.get called with right args
    get_mixin.assert_awaited_once_with(model_id)

    # Assert UpdateMixin.update called with right args
    data = model.model_dump(exclude={"id"}, exclude_none=True)
    data |= partial_params.model_dump(exclude_none=True)
    update_mixin.assert_awaited_once_with(model_id, full_params_cls(**data))

    # Assert result
    assert result
