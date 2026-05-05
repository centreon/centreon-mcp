from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel

from centreon_mcp.types.base import ResourceType
from centreon_mcp.types.host import HostStatus
from centreon_mcp.types.service import ServiceStatus
from centreon_mcp.utils.request import request

ResourceStatus = HostStatus | ServiceStatus


class Status(BaseModel):
    code: int
    name: ResourceStatus
    severity_code: int


class Resource(BaseModel):
    endpoint: ClassVar[str] = "monitoring/resources"

    uuid: str
    id: int
    type: ResourceType
    name: str
    alias: str | None
    fqdn: str | None
    host_id: int
    service_id: int | None
    monitoring_server_name: str
    is_in_downtime: bool
    is_acknowledged: bool
    is_in_flapping: bool
    status: Status
    information: str | None
    has_active_checks_enabled: bool
    has_passive_checks_enabled: bool
    last_status_change: datetime | None
    last_check: str | None
    tries: str | None

    @classmethod
    async def list(
        cls,
        search: str,
        types: str,
        statuses: str | None = None,
        hostgroup_names: str | None = None,
        servicegroup_names: str | None = None,
        host_category_names: str | None = None,
        service_category_names: str | None = None,
        monitoring_server_names: str | None = None,
        status_types: str | None = None,
        limit: int | None = None,
        page: int | None = None,
        sort_by: str | None = None,
    ) -> list["Resource"]:
        """
        List ressources (hosts and services) in real-time monitoring.
        """
        params = {
            "search": search,
            "limit": limit,
            "page": page,
            "sort_by": sort_by,
            "types": types,
            "statuses": statuses,
            "hostgroup_names": hostgroup_names,
            "servicegroup_names": servicegroup_names,
            "host_category_names": host_category_names,
            "service_category_names": service_category_names,
            "monitoring_server_names": monitoring_server_names,
            "status_types": status_types,
        }
        content = await request("GET", cls.endpoint, params=params)
        return [cls(**item) for item in content["result"]]
