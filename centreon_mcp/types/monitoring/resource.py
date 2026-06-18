from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel

from centreon_mcp.types.base import ResourceType, Status
from centreon_mcp.utils.mixins import ListMixin


class Resource(BaseModel, ListMixin):
    endpoint: ClassVar[str] = "monitoring/resources"

    uuid: str
    id: int
    type: ResourceType
    name: str
    alias: str | None = None
    fqdn: str | None = None
    host_id: int
    service_id: int | None = None
    monitoring_server_name: str
    is_in_downtime: bool
    is_acknowledged: bool
    is_in_flapping: bool
    status: Status
    information: str | None = None
    has_active_checks_enabled: bool
    has_passive_checks_enabled: bool
    last_status_change: datetime | None = None
    last_check: str | None = None
    tries: str | None = None
