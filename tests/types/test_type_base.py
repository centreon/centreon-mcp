from unittest.mock import AsyncMock, patch

import pytest
from pydantic import BaseModel

from centreon_mcp.types.base import BaseResource, CentreonBaseModel, StatusCount
from centreon_mcp.types.downtime import Downtime
from centreon_mcp.types.host import HostConfiguration
from centreon_mcp.types.host_category import (
    HostCategoryConfiguration,
    HostCategoryConfigurationFullParams,
)
from centreon_mcp.types.host_group import HostGroupConfiguration
from centreon_mcp.types.host_severity import HostSeverity, HostSeverityFullParams

MODULE = "centreon_mcp.types.base"


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


async def test_base_resource_dump():

    # Setup args
    resource_type = "service"
    resource_id = 20
    host_id = 10
    resource = BaseResource(type=resource_type, resource_id=resource_id, host_id=host_id)

    # Call test method
    result = resource.dump()

    # Assert result
    assert result == {"parent": {"id": host_id}, "id": resource_id, "type": resource_type}


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
async def test_centreon_base_model_delete(
    request: AsyncMock, model: CentreonBaseModel, endpoint: str
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
    "endpoint,model,params",
    [
        (
            "configuration/hosts/categories",
            HostCategoryConfiguration,
            HostCategoryConfigurationFullParams.model_construct(),
        ),
        (
            "configuration/hosts/groups",
            HostGroupConfiguration,
            HostCategoryConfigurationFullParams.model_construct(),
        ),
        ("configuration/hosts/severities", HostSeverity, HostSeverityFullParams.model_construct()),
    ],
)
@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_centreon_base_model_update(
    request: AsyncMock, endpoint: str, model: CentreonBaseModel, params: BaseModel
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
    "endpoint,model,payload",
    [
        (
            "configuration/hosts/categories",
            HostCategoryConfiguration,
            {
                "id": 10,
                "name": "host_category_name",
                "alias": "host_category_alias",
                "is_activated": True,
            },
        ),
        (
            "configuration/hosts/groups",
            HostGroupConfiguration,
            {
                "id": 10,
                "name": "host_group_name",
                "is_activated": True,
                "enabled_hosts_count": 10,
                "disabled_hosts_count": 10,
            },
        ),
        (
            "configuration/hosts/severities",
            HostSeverity,
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
async def test_centreon_base_model_get(
    request: AsyncMock, endpoint: str, model: CentreonBaseModel, payload: dict
):

    # Setup args
    model_id = 10

    # Mock request
    instance = model.model_construct(**payload)
    request.return_value = instance.model_dump(mode="json")

    # Call test function
    result = await model.get(model_id)

    # Assert request called with right args
    request.assert_awaited_once_with("GET", f"{endpoint}/{model_id}")

    # Assert result
    assert result == instance
