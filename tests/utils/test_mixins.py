from unittest.mock import AsyncMock, patch

import pytest
from pydantic import BaseModel

from centreon_mcp.types.downtime import Downtime
from centreon_mcp.types.host import HostConfiguration, HostConfigurationPartialParams
from centreon_mcp.types.host_category import (
    HostCategoryConfiguration,
    HostCategoryConfigurationFullParams,
)
from centreon_mcp.types.host_group import HostGroupConfiguration, HostGroupConfigurationFullParams
from centreon_mcp.types.host_severity import HostSeverity, HostSeverityFullParams
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, PatchMixin, ReadMixin, UpdateMixin

MODULE = "centreon_mcp.utils.mixins"


@pytest.mark.parametrize(
    "model,params,endpoint",
    [
        (
            HostCategoryConfiguration,
            HostCategoryConfigurationFullParams.model_construct(),
            "configuration/hosts/categories",
        ),
        (
            HostGroupConfiguration,
            HostGroupConfigurationFullParams.model_construct(),
            "configuration/hosts/groups",
        ),
        (HostSeverity, HostSeverityFullParams.model_construct(), "configuration/hosts/severities"),
    ],
)
@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_create_mixin[CentreonModel: CreateMixin](
    request: AsyncMock, model: type[CentreonModel], params: BaseModel, endpoint: str
):

    # Mock request
    request.return_value = None

    # Call test function
    await model.create(params)

    # Assert request called with right args
    payload = params.model_dump(mode="json", exclude_none=True)
    request.assert_awaited_once_with("POST", endpoint, payload)


@pytest.mark.parametrize(
    "model,endpoint",
    [
        (HostConfiguration, "configuration/hosts"),
        (HostGroupConfiguration, "configuration/hosts/groups"),
        (HostCategoryConfiguration, "configuration/hosts/categories"),
        (HostSeverity, "configuration/hosts/severities"),
        (Downtime, "monitoring/downtimes"),
    ],
)
@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_delete_mixin[CentreonModel: DeleteMixin](
    request: AsyncMock, model: CentreonModel, endpoint: str
):

    # Setup args
    model_id = 10

    # Mock request
    request.return_value = None

    # Call test function
    await model.delete(model_id)

    # Assert request called with right args
    request.assert_awaited_once_with("DELETE", f"{endpoint}/{model_id}")


@pytest.mark.parametrize(
    "model,params,endpoint",
    [
        (
            HostCategoryConfiguration,
            HostCategoryConfigurationFullParams.model_construct(),
            "configuration/hosts/categories",
        ),
        (
            HostGroupConfiguration,
            HostGroupConfigurationFullParams.model_construct(),
            "configuration/hosts/groups",
        ),
        (HostSeverity, HostSeverityFullParams.model_construct(), "configuration/hosts/severities"),
    ],
)
@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_update_mixin[CentreonModel: UpdateMixin](
    request: AsyncMock, model: CentreonModel, params: BaseModel, endpoint: str
):

    # Setup args
    model_id = 10

    # Mock request
    request.return_value = None

    # Call test function
    await model.update(model_id, params)

    # Assert request called with right args
    payload = params.model_dump(mode="json", exclude_none=True)
    request.assert_awaited_once_with("PUT", f"{endpoint}/{model_id}", payload)


@pytest.mark.parametrize(
    "model,endpoint,payload",
    [
        (
            HostCategoryConfiguration,
            "configuration/hosts/categories",
            {
                "id": 10,
                "name": "host_category_name",
                "alias": "host_category_alias",
                "is_activated": True,
            },
        ),
        (
            HostGroupConfiguration,
            "configuration/hosts/groups",
            {
                "id": 10,
                "name": "host_group_name",
                "is_activated": True,
                "enabled_hosts_count": 10,
                "disabled_hosts_count": 10,
            },
        ),
        (
            HostSeverity,
            "configuration/hosts/severities",
            {
                "id": 10,
                "name": "host_severity_name",
                "alias": "host_severity_alias",
                "level": 10,
                "icon_id": 1,
                "is_activated": True,
            },
        ),
    ],
)
@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_get_mixin[CentreonModel: ReadMixin](
    request: AsyncMock, model: type[CentreonModel], endpoint: str, payload: dict
):

    # Setup args
    model_id = 10

    # Mock request
    request.return_value = payload

    # Call test function
    result = await model.get(model_id)

    # Assert request called with right args
    request.assert_awaited_once_with("GET", f"{endpoint}/{model_id}")

    # Assert result
    assert result == model(**payload)


@pytest.mark.parametrize(
    "model,params,endpoint",
    [
        (
            HostConfiguration,
            HostConfigurationPartialParams.model_construct(),
            "configuration/hosts",
        )
    ],
)
@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_patch_mixin[CentreonModel: PatchMixin](
    request: AsyncMock, model: CentreonModel, params: BaseModel, endpoint: str
):

    # Setup args
    model_id = 10

    # Mock request
    request.return_value = None

    # Call test function
    await model.patch(model_id, params)

    # Assert request called with right args
    payload = params.model_dump(mode="json", exclude_none=True)
    request.assert_awaited_once_with("PATCH", f"{endpoint}/{model_id}", payload)
