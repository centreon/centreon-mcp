import pytest

from centreon_mcp.types.configuration.command import (
    Command,
    CommandFilter,
    CommandOrder,
    CommandParams,
)
from centreon_mcp.types.configuration.host import (
    Host,
    HostFilter,
    HostFullParams,
    HostOrder,
    HostPartialParams,
)
from centreon_mcp.types.configuration.host_category import (
    HostCategory,
    HostCategoryFilter,
    HostCategoryFullParams,
    HostCategoryOrder,
    HostCategoryPartialParams,
)
from centreon_mcp.types.configuration.host_group import (
    HostGroup,
    HostGroupFilter,
    HostGroupFullParams,
    HostGroupOrder,
    HostGroupPartialParams,
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
    MonitoringServer,
    MonitoringServerFilter,
    MonitoringServerOrder,
)
from centreon_mcp.types.configuration.service import (
    Service,
    ServiceFilter,
    ServiceFullParams,
    ServiceOrder,
    ServicePartialParams,
)
from centreon_mcp.types.configuration.service_category import (
    ServiceCategory,
    ServiceCategoryFilter,
    ServiceCategoryFullParams,
    ServiceCategoryOrder,
)
from centreon_mcp.types.configuration.service_group import (
    ServiceGroup,
    ServiceGroupFilter,
    ServiceGroupFullParams,
    ServiceGroupOrder,
)
from centreon_mcp.types.configuration.service_severity import (
    ServiceSeverity,
    ServiceSeverityFilter,
    ServiceSeverityFullParams,
    ServiceSeverityOrder,
    ServiceSeverityPartialParams,
)
from centreon_mcp.types.configuration.service_template import (
    ServiceTemplate,
    ServiceTemplateFilter,
    ServiceTemplateFullParams,
    ServiceTemplateOrder,
    ServiceTemplatePartialParams,
)
from centreon_mcp.types.configuration.time_period import (
    TimePeriod,
    TimePeriodDay,
    TimePeriodFilter,
    TimePeriodFullParams,
    TimePeriodOrder,
    TimePeriodPartialParams,
    WeekDay,
)

from .base import (
    TestCreateMixinBase,
    TestDeleteMixinBase,
    TestListMixinBase,
    TestPatchMixinBase,
    TestPutMixinBase,
    TestReadMixinBase,
)

MODULE = "centreon_mcp.utils.mixins"


@pytest.mark.parametrize(
    "model,params,endpoint",
    [
        (
            Host,
            HostFullParams.model_construct(),
            "configuration/hosts",
        ),
        (
            HostCategory,
            HostCategoryFullParams.model_construct(),
            "configuration/hosts/categories",
        ),
        (
            HostGroup,
            HostGroupFullParams.model_construct(),
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
        (Service, ServiceFullParams.model_construct(), "configuration/services"),
        (ServiceGroup, ServiceGroupFullParams.model_construct(), "configuration/services/groups"),
        (
            ServiceCategory,
            ServiceCategoryFullParams.model_construct(),
            "configuration/services/categories",
        ),
        (
            ServiceTemplate,
            ServiceTemplateFullParams.model_construct(),
            "configuration/services/templates",
        ),
        (
            ServiceSeverity,
            ServiceSeverityFullParams.model_construct(),
            "configuration/services/severities",
        ),
        (Command, CommandParams.model_construct(), "configuration/commands"),
        (TimePeriod, TimePeriodFullParams.model_construct(), "configuration/timeperiods"),
    ],
)
class TestCreateMixinConfiguration(TestCreateMixinBase):
    __test__ = True


@pytest.mark.parametrize(
    "model,endpoint",
    [
        (Host, "configuration/hosts"),
        (HostGroup, "configuration/hosts/groups"),
        (HostCategory, "configuration/hosts/categories"),
        (HostSeverity, "configuration/hosts/severities"),
        (HostTemplate, "configuration/hosts/templates"),
        (Service, "configuration/services"),
        (ServiceGroup, "configuration/services/groups"),
        (ServiceCategory, "configuration/services/categories"),
        (ServiceTemplate, "configuration/services/templates"),
        (ServiceSeverity, "configuration/services/severities"),
        (TimePeriod, "configuration/timeperiods"),
    ],
)
class TestDeleteMixinConfiguration(TestDeleteMixinBase):
    __test__ = True


@pytest.mark.parametrize(
    "endpoint,model_cls,model,partial_params,full_params",
    [
        (
            "configuration/hosts/categories",
            HostCategory,
            HostCategory(
                id=10, name="host_category_name", alias="host_category_alias", is_activated=True
            ),
            HostCategoryPartialParams(
                name="new_host_category_name", comment="new_host_category_comment"
            ),
            HostCategoryFullParams(
                name="new_host_category_name",
                alias="host_category_alias",
                comment="new_host_category_comment",
                is_activated=True,
            ),
        ),
        (
            "configuration/hosts/groups",
            HostGroup,
            HostGroup(
                id=10,
                name="host_group_name",
                alias="host_group_alias",
                icon_id=5,
                is_activated=True,
                hosts=[{"id": 10}, {"id": 11}, {"id": 12}],  # type: ignore[list-item]
            ),
            HostGroupPartialParams(name="new_host_group_name", icon_id=10, hosts=[11, 12, 13]),
            HostGroupFullParams(
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
        (
            "configuration/services/severities",
            ServiceSeverity,
            ServiceSeverity(
                id=10, name="name", alias="alias", level=10, icon_id=5, is_activated=True
            ),
            ServiceSeverityPartialParams(alias="new_alias", level=20),
            ServiceSeverityFullParams(
                name="name", alias="new_alias", level=20, icon_id=5, is_activated=True
            ),
        ),
        (
            "configuration/timeperiods",
            TimePeriod,
            TimePeriod(
                id=5,
                name="name",
                alias="alias",
                templates=[],
                days=[TimePeriodDay(day=WeekDay.MONDAY, time_range="14:00-15:00")],
                exceptions=[],
            ),
            TimePeriodPartialParams(name="new_name"),
            TimePeriodFullParams(
                name="new_name",
                alias="alias",
                templates=[],
                days=[TimePeriodDay(day=WeekDay.MONDAY, time_range="14:00-15:00")],
                exceptions=[],
            ),
        ),
    ],
)
class TestPutMixinConfiguration(TestPutMixinBase):
    __test__ = True


@pytest.mark.parametrize(
    "model,params,endpoint",
    [
        (
            Host,
            HostPartialParams.model_construct(),
            "configuration/hosts",
        ),
        (
            HostTemplate,
            HostTemplatePartialParams.model_construct(),
            "configuration/hosts/templates",
        ),
        (Service, ServicePartialParams.model_construct(), "configuration/services"),
        (
            ServiceTemplate,
            ServiceTemplatePartialParams.model_construct(),
            "configuration/services/templates",
        ),
    ],
)
class TestPatchMixinConfiguration(TestPatchMixinBase):
    __test__ = True


@pytest.mark.parametrize(
    "model,endpoint,payload",
    [
        (
            HostCategory,
            "configuration/hosts/categories",
            {
                "id": 10,
                "name": "host_category_name",
                "alias": "host_category_alias",
                "is_activated": True,
            },
        ),
        (
            HostGroup,
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
            ServiceSeverity,
            "configuration/services/severities",
            {
                "id": 10,
                "name": "name",
                "alias": "alias",
                "level": 10,
                "icon_id": 1,
                "is_activated": True,
            },
        ),
        (
            TimePeriod,
            "configuration/timeperiods",
            {
                "id": 5,
                "name": "name",
                "alias": "alias",
                "templates": [],
                "days": [{"day": 1, "time_range": "15:00-16:00"}],
                "exceptions": [{"day_range": "2026-08-14", "time_range": "10:00-18:00"}],
            },
        ),
    ],
)
class TestReadMixinConfiguration(TestReadMixinBase):
    __test__ = True


@pytest.mark.parametrize(
    "model,filters,order,search,sort_by,endpoint,payload",
    [
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
            Host,
            [HostFilter(host_configuration_name="host_name")],
            HostOrder(order="DESC", field="address"),
            '{"$or": [{"$and": [{"name": {"$eq": "host_name"}}]}]}',
            '{"order":"DESC","field":"address"}',
            "configuration/hosts",
            {
                "id": 10,
                "name": "host_name",
                "alias": "host_alias",
                "address": "127.0.0.1",
                "monitoring_server": {"id": 1, "name": "poller_name"},
                "templates": [],
                "categories": [],
                "groups": [],
                "is_activated": True,
            },
        ),
        (
            HostCategory,
            [HostCategoryFilter(host_category_name="host_category_name")],
            HostCategoryOrder(order="DESC", field="alias"),
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
            HostGroup,
            [HostGroupFilter(host_group_alias="host_group_alias")],
            HostGroupOrder(order="ASC", field="is_activated"),
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
            MonitoringServer,
            [MonitoringServerFilter(monitoring_server_name="poller_name")],
            MonitoringServerOrder(order="ASC", field="name"),
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
        (
            Service,
            [ServiceFilter(name="service_name", severity_id=10)],
            ServiceOrder(order="DESC", field="name"),
            '{"$or": [{"$and": [{"name": {"$eq": "service_name"}}, {"severity.id": {"$eq": 10}}]}]}',
            '{"order":"DESC","field":"name"}',
            "configuration/services",
            {
                "id": 10,
                "name": "service_name",
                "categories": [],
                "groups": [],
                "is_activated": True,
            },
        ),
        (
            ServiceGroup,
            [ServiceGroupFilter(service_group_name="service_group_name", host_group_id=10)],
            ServiceGroupOrder(field="name"),
            '{"$or": [{"$and": [{"name": {"$eq": "service_group_name"}}, {"hostgroup.id": {"$eq": 10}}]}]}',
            '{"order":"ASC","field":"name"}',
            "configuration/services/groups",
            {
                "id": 10,
                "name": "service_group_name",
                "alias": "service_group_alias",
                "is_activated": True,
            },
        ),
        (
            ServiceCategory,
            [ServiceCategoryFilter(service_category_alias="service_category_alias", host_id=10)],
            ServiceCategoryOrder(field="alias"),
            '{"$or": [{"$and": [{"alias": {"$eq": "service_category_alias"}}, {"host.id": {"$eq": 10}}]}]}',
            '{"order":"ASC","field":"alias"}',
            "configuration/services/categories",
            {
                "id": 10,
                "name": "service_category_name",
                "alias": "service_category_alias",
                "is_activated": True,
            },
        ),
        (
            ServiceTemplate,
            [ServiceTemplateFilter(service_template_name="service_template_name")],
            ServiceTemplateOrder(field="alias"),
            '{"$or": [{"$and": [{"name": {"$eq": "service_template_name"}}]}]}',
            '{"order":"ASC","field":"alias"}',
            "configuration/services/templates",
            {
                "id": 10,
                "name": "service_template_name",
                "alias": "service_template_alias",
                "is_locked": False,
            },
        ),
        (
            ServiceSeverity,
            [ServiceSeverityFilter(service_severity_name="name")],
            ServiceSeverityOrder(field="alias"),
            '{"$or": [{"$and": [{"name": {"$eq": "name"}}]}]}',
            '{"order":"ASC","field":"alias"}',
            "configuration/services/severities",
            {
                "id": 10,
                "name": "name",
                "alias": "alias",
                "level": 10,
                "icon_id": 1,
                "is_activated": False,
            },
        ),
        (
            TimePeriod,
            [TimePeriodFilter(time_period_alias="alias")],
            TimePeriodOrder(field="name"),
            '{"$or": [{"$and": [{"alias": {"$eq": "alias"}}]}]}',
            '{"order":"ASC","field":"name"}',
            "configuration/timeperiods",
            {
                "id": 5,
                "name": "name",
                "alias": "alias",
                "templates": [],
                "days": [{"day": 1, "time_range": "15:00-16:00"}],
                "exceptions": [{"day_range": "2026-08-14", "time_range": "10:00-18:00"}],
            },
        ),
    ],
)
class TestListMixinConfiguration(TestListMixinBase):
    __test__ = True
