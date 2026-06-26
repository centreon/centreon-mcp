from unittest.mock import AsyncMock, patch

import pytest
from pydantic import BaseModel

from centreon_mcp.types.configuration.command import Command, CommandParams
from centreon_mcp.types.configuration.host import HostConfiguration, HostConfigurationPartialParams
from centreon_mcp.types.configuration.host_category import (
    HostCategoryConfiguration,
    HostCategoryConfigurationFullParams,
)
from centreon_mcp.types.configuration.host_group import (
    HostGroupConfiguration,
    HostGroupConfigurationFullParams,
)
from centreon_mcp.types.configuration.host_severity import HostSeverity, HostSeverityFullParams
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
from centreon_mcp.utils.mixins import (
    CreateMixin,
    DeleteMixin,
    ListMixin,
    PatchMixin,
    ReadMixin,
    UpdateMixin,
)

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
        (HostTemplate, HostTemplateFullParams.model_construct(), "configuration/hosts/templates"),
        (Command, CommandParams.model_construct(), "configuration/commands"),
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
    payload = params.model_dump(mode="json", exclude_none=True, exclude={"model_type"})
    request.assert_awaited_once_with("POST", endpoint, payload)


@pytest.mark.parametrize(
    "model,endpoint",
    [
        (HostConfiguration, "configuration/hosts"),
        (HostGroupConfiguration, "configuration/hosts/groups"),
        (HostCategoryConfiguration, "configuration/hosts/categories"),
        (HostSeverity, "configuration/hosts/severities"),
        (Downtime, "monitoring/downtimes"),
        (HostTemplate, "configuration/hosts/templates"),
    ],
)
@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_delete_mixin[CentreonModel: DeleteMixin](
    request: AsyncMock, model: type[CentreonModel], endpoint: str
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
    request: AsyncMock, model: type[CentreonModel], params: BaseModel, endpoint: str
):

    # Setup args
    model_id = 10

    # Mock request
    request.return_value = None

    # Call test function
    await model.update(model_id, params)

    # Assert request called with right args
    payload = params.model_dump(mode="json", exclude_none=True, exclude={"model_type"})
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
        ),
        (
            HostTemplate,
            HostTemplatePartialParams.model_construct(),
            "configuration/hosts/templates",
        ),
    ],
)
@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_patch_mixin[CentreonModel: PatchMixin](
    request: AsyncMock, model: type[CentreonModel], params: BaseModel, endpoint: str
):

    # Setup args
    model_id = 10

    # Mock request
    request.return_value = None

    # Call test function
    await model.patch(model_id, params)

    # Assert request called with right args
    payload = params.model_dump(mode="json", exclude_none=True, exclude={"model_type"})
    request.assert_awaited_once_with("PATCH", f"{endpoint}/{model_id}", payload)


@pytest.mark.parametrize(
    "model,endpoint,payload",
    [
        (
            Acknowledgement,
            "monitoring/acknowledgements",
            {
                "id": 10,
                "host_id": 10,
                "service_id": 10,
                "author_id": 10,
                "author_name": "author_name",
                "comment": "comment",
                "deletion_time": "2026-05-28T10:00:00",
                "entry_time": "2026-05-28T10:00:00",
                "is_notify_contacts": True,
                "is_persistent_comment": True,
                "is_sticky": True,
                "type": 1,
            },
        ),
        (
            Downtime,
            "monitoring/downtimes",
            {
                "id": 10,
                "author_id": 10,
                "author_name": "author_name",
                "host_id": 10,
                "poller_id": 10,
                "comment": "comment",
                "is_started": True,
                "is_fixed": True,
                "is_cancelled": False,
            },
        ),
        (
            Command,
            "configuration/commands",
            {
                "id": 10,
                "name": "command_name",
                "type": 2,
                "command_line": "command_line",
                "is_activated": True,
                "is_shell": True,
                "is_locked": False,
            },
        ),
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
        (
            ServiceGroup,
            "monitoring/servicegroups",
            {
                "id": 10,
                "name": "service_group_name",
            },
        ),
        (
            MonitoringServer,
            "monitoring/servers",
            {"id": 10, "name": "monitoring_server_name", "is_running": True},
        ),
        (
            HostTemplate,
            "configuration/hosts/templates",
            {
                "id": 10,
                "name": "host_template_name",
                "alias": "host_template_alias",
                "is_locked": True,
            },
        ),
        (
            Resource,
            "monitoring/resources",
            {
                "id": 10,
                "uuid": "resource_uuid",
                "type": "host",
                "name": "resource_name",
                "host_id": 10,
                "monitoring_server_name": "poller_name",
                "is_in_downtime": False,
                "is_acknowledged": False,
                "is_in_flapping": False,
                "status": {"code": 0, "severity_code": 0, "name": "UP"},
                "has_active_checks_enabled": False,
                "has_passive_checks_enabled": False,
            },
        ),
        (
            MonitoringServerConfiguration,
            "configuration/monitoring-servers",
            {
                "id": 10,
                "name": "monitoring_server_name",
                "address": "",
                "is_localhost": True,
                "is_default": True,
                "ssh_port": 0,
                "engine_start_command": "",
                "engine_stop_command": "",
                "engine_restart_command": "",
                "engine_reload_command": "",
                "nagios_bin": "",
                "nagiostats_bin": "",
                "broker_reload_command": "",
                "init_script_centreontrapd": "",
                "snmp_trapd_path_conf": "",
                "remote_server_use_as_proxy": True,
                "is_updated": True,
                "is_activate": True,
            },
        ),
    ],
)
@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_list_mixin[CentreonModel: ListMixin](
    request: AsyncMock, model: type[CentreonModel], endpoint: str, payload: dict
):

    # Setup args
    search = ""
    limit = 50
    page = 1
    sort_by = ""

    # Mock request
    request.return_value = {"result": [payload]}

    # Call test function
    results = await model.list(search, limit, page, sort_by)

    # Assert request called with right args
    params = {"search": search, "limit": limit, "page": page, "sort_by": sort_by}
    request.assert_awaited_once_with("GET", endpoint, params=params)

    # Assert result
    assert results == [model(**payload)]
