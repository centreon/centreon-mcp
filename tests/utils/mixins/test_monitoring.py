from datetime import datetime

import pytest

from centreon_mcp.types.monitoring.acknowledgement import (
    Acknowledgement,
    AcknowledgementFilter,
    AcknowledgementOrder,
    AcknowledgementParams,
)
from centreon_mcp.types.monitoring.check import Check, CheckParams
from centreon_mcp.types.monitoring.downtime import (
    Downtime,
    DowntimeFilter,
    DowntimeOrder,
    DowntimeParams,
)
from centreon_mcp.types.monitoring.host_group import HostGroup, HostGroupFilter, HostGroupOrder
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

from .base import TestDeleteMixinBase, TestListMixinBase, TestSetMixinBase

MODULE = "centreon_mcp.utils.mixins"


@pytest.mark.parametrize(
    "model,endpoint",
    [
        (Downtime, "monitoring/downtimes"),
    ],
)
class TestDeleteMixinMonitoring(TestDeleteMixinBase):
    __test__ = True


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
            MonitoringServer,
            [MonitoringServerFilter(monitoring_server_id=10, monitoring_server_name="poller_name")],
            MonitoringServerOrder(order="ASC", field="name"),
            '{"$or": [{"$and": [{"id": {"$eq": 10}}, {"name": {"$eq": "poller_name"}}]}]}',
            '{"order":"ASC","field":"name"}',
            "monitoring/servers",
            {"id": 10, "name": "monitoring_server_name", "is_running": True},
        ),
        (
            HostGroup,
            [HostGroupFilter(poller_id=10, host_address="host_address")],
            HostGroupOrder(order="ASC", field="host.state"),
            '{"$or": [{"$and": [{"host.address": {"$eq": "host_address"}}, {"poller.id": {"$eq": 10}}]}]}',
            '{"order":"ASC","field":"host.state"}',
            "monitoring/hostgroups",
            {
                "id": 10,
                "name": "HOST_group_name",
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
    ],
)
class TestListMixinMonitoring(TestListMixinBase):
    __test__ = True


@pytest.mark.parametrize(
    "model,params,endpoint,payload",
    [
        (
            Acknowledgement,
            AcknowledgementParams(comment="comment"),
            "monitoring/acknowledgements",
            {
                "acknowledgement": {
                    "comment": "comment",
                    "with_services": True,
                    "is_notify_contacts": True,
                    "is_persistent_comment": True,
                    "is_sticky": True,
                    "force_active_checks": True,
                },
            },
        ),
        (
            Downtime,
            DowntimeParams(
                start_time=datetime(2026, 7, 21),
                end_time=datetime(2026, 7, 21),
                is_fixed=True,
                duration=3600,
                comment="comment",
                with_services=True,
            ),
            "monitoring/downtimes",
            {
                "downtime": {
                    "start_time": "2026-07-21T00:00:00",
                    "end_time": "2026-07-21T00:00:00",
                    "is_fixed": True,
                    "duration": 3600,
                    "comment": "comment",
                    "with_services": True,
                },
            },
        ),
        (
            Check,
            CheckParams(is_forced=True),
            "monitoring/resources/check",
            {
                "check": {"is_forced": True},
            },
        ),
    ],
)
class TestSetMixinMonitoring(TestSetMixinBase):
    __test__ = True
