from collections.abc import Sequence
from unittest.mock import AsyncMock, patch

import pytest
from pydantic import BaseModel

from centreon_mcp.types.configuration.command import (
    Command,
    CommandFilter,
    CommandOrder,
    CommandParams,
)
from centreon_mcp.types.configuration.host import (
    HostConfiguration,
    HostConfigurationPartialParams,
)
from centreon_mcp.types.configuration.host_category import (
    HostCategoryConfiguration,
    HostCategoryConfigurationFilter,
    HostCategoryConfigurationFullParams,
    HostCategoryConfigurationOrder,
    HostCategoryConfigurationPartialParams,
)
from centreon_mcp.types.configuration.host_group import (
    HostGroupConfiguration,
    HostGroupConfigurationFilter,
    HostGroupConfigurationFullParams,
    HostGroupConfigurationOrder,
    HostGroupConfigurationPartialParams,
)
from centreon_mcp.types.configuration.host_severity import (
    HostSeverity,
    HostSeverityFilter,
    HostSeverityFullParams,
    HostSeverityOrder,
    HostSeverityPartialParams,
)
from centreon_mcp.types.configuration.host_template import (
    HostTemplate,
    HostTemplateFilter,
    HostTemplateFullParams,
    HostTemplateOrder,
    HostTemplatePartialParams,
)
from centreon_mcp.types.configuration.monitoring_server import (
    MonitoringServerConfiguration,
    MonitoringServerConfigurationFilter,
    MonitoringServerConfigurationOrder,
)
from centreon_mcp.types.monitoring.acknowledgement import (
    Acknowledgement,
    AcknowledgementFilter,
    AcknowledgementOrder,
)
from centreon_mcp.types.monitoring.downtime import Downtime, DowntimeFilter, DowntimeOrder
from centreon_mcp.types.monitoring.monitoring_server import (
    MonitoringServer,
    MonitoringServerFilter,
    MonitoringServerOrder,
)
from centreon_mcp.types.monitoring.resource import Resource, ResourceFilter, ResourceOrder
from centreon_mcp.types.monitoring.servicegroup import (
    ServiceGroup,
    ServiceGroupFilter,
    ServiceGroupOrder,
)
from centreon_mcp.utils.base import BaseFilter, BaseOrder
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
    "model,filters,order,search,sort_by,endpoint,payload",
    [
        (
            Acknowledgement,
            [AcknowledgementFilter()],
            AcknowledgementOrder(order="ASC", field="host.state"),
            '{"$or": []}',
            '{"order":"ASC","field":"host.state"}',
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
            [DowntimeFilter(host_name="host_name", is_fixed=True)],
            DowntimeOrder(order="DESC", field="start_time"),
            '{"$or": [{"$and": [{"host.name": {"$eq": "host_name"}}, {"is_fixed": {"$eq": true}}]}]}',
            '{"order":"DESC","field":"start_time"}',
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
            [CommandFilter(command_name="command_name", command_is_locked=False)],
            CommandOrder(order="ASC", field="name"),
            '{"$or": [{"$and": [{"name": {"$eq": "command_name"}}, {"is_locked": {"$eq": false}}]}]}',
            '{"order":"ASC","field":"name"}',
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
            [HostCategoryConfigurationFilter(host_category_name="host_category_name")],
            HostCategoryConfigurationOrder(order="DESC", field="alias"),
            '{"$or": [{"$and": [{"name": {"$eq": "host_category_name"}}]}]}',
            '{"order":"DESC","field":"alias"}',
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
            [HostGroupConfigurationFilter(host_group_alias="host_group_alias")],
            HostGroupConfigurationOrder(order="ASC", field="is_activated"),
            '{"$or": [{"$and": [{"alias": {"$eq": "host_group_alias"}}]}]}',
            '{"order":"ASC","field":"is_activated"}',
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
            [HostSeverityFilter(host_severity_id=10, min_host_severity_level=30)],
            HostSeverityOrder(order="DESC", field="level"),
            '{"$or": [{"$and": [{"id": {"$eq": 10}}, {"level": {"$ge": 30}}]}]}',
            '{"order":"DESC","field":"level"}',
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
            [ServiceGroupFilter(poller_id=10, host_address="host_address")],
            ServiceGroupOrder(order="ASC", field="host.state"),
            '{"$or": [{"$and": [{"host.address": {"$eq": "host_address"}}, {"poller.id": {"$eq": 10}}]}]}',
            '{"order":"ASC","field":"host.state"}',
            "monitoring/servicegroups",
            {
                "id": 10,
                "name": "service_group_name",
            },
        ),
        (
            MonitoringServer,
            [MonitoringServerFilter(monitoring_server_name="poller_name")],
            MonitoringServerOrder(order="DESC", field="running"),
            '{"$or": [{"$and": [{"name": {"$eq": "poller_name"}}]}]}',
            '{"order":"DESC","field":"running"}',
            "monitoring/servers",
            {"id": 10, "name": "monitoring_server_name", "is_running": True},
        ),
        (
            HostTemplate,
            [HostTemplateFilter(host_template_alias="host_template_alias")],
            HostTemplateOrder(order="ASC", field="name"),
            '{"$or": [{"$and": [{"alias": {"$eq": "host_template_alias"}}]}]}',
            '{"order":"ASC","field":"name"}',
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
            [ResourceFilter(parent_name="parent_name", information_like="info_like")],
            ResourceOrder(order="DESC", field="host.address"),
            '{"$or": [{"$and": [{"parent_name": {"$lk": "parent_name"}}, {"information": {"$lk": "info_like"}}]}]}',
            '{"order":"DESC","field":"host.address"}',
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
            [MonitoringServerConfigurationFilter(monitoring_server_name="poller_name")],
            MonitoringServerConfigurationOrder(order="ASC", field="name"),
            '{"$or": [{"$and": [{"name": {"$eq": "poller_name"}}]}]}',
            '{"order":"ASC","field":"name"}',
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
        self,
        request: AsyncMock,
        model: type[ListMixin],
        filters: Sequence[BaseFilter],
        order: BaseOrder,
        search: str,
        sort_by: str,
        endpoint: str,
        payload: dict,
    ):

        # Setup args
        limit = 10
        page = 1

        # Mock request
        request.return_value = {"result": [payload]}

        # Call test function
        results = await model.list(filters, limit, page, order)

        # Assert request called with right args
        params = {"search": search, "limit": limit, "page": page, "sort_by": sort_by}
        request.assert_awaited_once_with("GET", endpoint, params=params)

        # Assert result
        assert results == [model(**payload)]
