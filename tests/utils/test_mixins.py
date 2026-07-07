import json
from unittest.mock import AsyncMock, patch

import pytest
from pydantic import BaseModel

from centreon_mcp.types.base import BaseFilter, BaseOrder
from centreon_mcp.types.configuration.command import Command, CommandParams
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
from centreon_mcp.utils.mixins import (
    CreateMixin,
    DeleteMixin,
    ListMixin,
    PatchMixin,
    PutMixin,
    ReadMixin,
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
        (
            HostSeverity,
            HostSeverityFullParams.model_construct(),
            "configuration/hosts/severities",
        ),
        (
            HostTemplate,
            HostTemplateFullParams.model_construct(),
            "configuration/hosts/templates",
        ),
        (Command, CommandParams.model_construct(), "configuration/commands"),
    ],
)
class TestCreateMixin:
    @patch(f"{MODULE}.request", new_callable=AsyncMock)
    async def test_create(
        self, request: AsyncMock, model: type[CreateMixin], params: BaseModel, endpoint: str
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
class TestDeleteMixin:
    @patch(f"{MODULE}.request", new_callable=AsyncMock)
    async def test_delete(self, request: AsyncMock, model: type[DeleteMixin], endpoint: str):

        # Setup args
        model_id = 10

        # Mock request
        request.return_value = None

        # Call test function
        await model.delete(model_id)

        # Assert request called with right args
        request.assert_awaited_once_with("DELETE", f"{endpoint}/{model_id}")


@pytest.mark.parametrize(
    "endpoint,model_cls,model,partial_params,full_params",
    [
        (
            "configuration/hosts/categories",
            HostCategoryConfiguration,
            HostCategoryConfiguration(
                id=10, name="host_category_name", alias="host_category_alias", is_activated=True
            ),
            HostCategoryConfigurationPartialParams(
                name="new_host_category_name", comment="new_host_category_comment"
            ),
            HostCategoryConfigurationFullParams(
                name="new_host_category_name",
                alias="host_category_alias",
                comment="new_host_category_comment",
                is_activated=True,
            ),
        ),
        (
            "configuration/hosts/groups",
            HostGroupConfiguration,
            HostGroupConfiguration(
                id=10,
                name="host_group_name",
                alias="host_group_alias",
                icon_id=5,
                is_activated=True,
                hosts=[{"id": 10}, {"id": 11}, {"id": 12}],  # type: ignore[list-item]
            ),
            HostGroupConfigurationPartialParams(
                name="new_host_group_name", icon_id=10, hosts=[11, 12, 13]
            ),
            HostGroupConfigurationFullParams(
                name="new_host_group_name",
                alias="host_group_alias",
                icon_id=10,
                geo_coords=None,
                comment=None,
                hosts=[11, 12, 13],
            ),
        ),
        (
            "configuration/hosts/severities",
            HostSeverity,
            HostSeverity(
                id=10,
                name="host_severity_name",
                alias="host_severity_alias",
                level=10,
                icon_id=5,
                is_activated=True,
            ),
            HostSeverityPartialParams(name="new_host_severity_name", is_activated=False),
            HostSeverityFullParams(
                name="new_host_severity_name",
                alias="host_severity_alias",
                level=10,
                icon_id=5,
                is_activated=False,
                comment=None,
            ),
        ),
    ],
)
class TestPutMixin:
    @patch(f"{MODULE}.request", new_callable=AsyncMock)
    async def test_put(
        self,
        request: AsyncMock,
        endpoint: str,
        model_cls: type[PutMixin],
        model: PutMixin,
        partial_params: BaseModel,
        full_params: BaseModel,
    ):
        # Setup args
        model_id = 10

        # Mock request
        request.return_value = None

        # Call test function
        await model_cls.put(model_id, full_params)

        # Assert request called with right args
        payload = full_params.model_dump(mode="json", exclude_none=True, exclude={"model_type"})
        request.assert_awaited_once_with("PUT", f"{endpoint}/{model_id}", payload)

    @patch(f"{MODULE}.PutMixin.put", new_callable=AsyncMock)
    @patch(f"{MODULE}.PutMixin.get", new_callable=AsyncMock)
    async def test_update(
        self,
        get_mixin: AsyncMock,
        put_mixin: AsyncMock,
        endpoint: str,
        model_cls: type[PutMixin],
        model: PutMixin,
        partial_params: BaseModel,
        full_params: BaseModel,
    ):
        # Setup args
        model_id = 10

        # Mock PutMixin.get
        get_mixin.return_value = model

        # Mock PutMixin.put
        put_mixin.return_value = True

        # Call the test method
        await model_cls.update(model_id, partial_params)

        # Assert ReadMixin.get awaited with correct args
        get_mixin.assert_awaited_once_with(model_id)

        # Assert PutMixin.put awaited with correct args
        put_mixin.assert_awaited_once_with(model_id, full_params)


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
class TestReadMixin:
    @patch(f"{MODULE}.request", new_callable=AsyncMock)
    async def test_get(
        self, request: AsyncMock, model: type[ReadMixin], endpoint: str, payload: dict
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
class TestPatchMixin:
    @patch(f"{MODULE}.request", new_callable=AsyncMock)
    async def test_patch_mixin(
        self, request: AsyncMock, model: type[PatchMixin], params: BaseModel, endpoint: str
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

    @patch(f"{MODULE}.PatchMixin.patch", new_callable=AsyncMock)
    async def test_update(
        self,
        patch_mixin: AsyncMock,
        model: type[PutMixin],
        params: BaseModel,
        endpoint: str,
    ):
        # Setup args
        model_id = 10

        # Mock PatchMixin.patch
        patch_mixin.return_value = None

        # Call test function
        await model.update(model_id, params)

        # Assert PatchMixin.patch called with right args
        patch_mixin.assert_awaited_once_with(model_id, params)


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
class TestListMixin:
    @patch(f"{MODULE}.request", new_callable=AsyncMock)
    async def test_list(
        self, request: AsyncMock, model: type[ListMixin], endpoint: str, payload: dict
    ):

        # Setup args
        filters = [BaseFilter()]
        limit = 10
        page = 1
        order = BaseOrder()

        # Mock request
        request.return_value = {"result": [payload]}

        # Call test function
        results = await model.list(filters, limit, page, order)

        # Assert request called with right args
        search = json.dumps(BaseFilter.join(filters))
        sort_by = order.model_dump_json(exclude={"model_type"})
        params = {"search": search, "limit": limit, "page": page, "sort_by": sort_by}
        request.assert_awaited_once_with("GET", endpoint, params=params)

        # Assert result
        assert results == [model(**payload)]
