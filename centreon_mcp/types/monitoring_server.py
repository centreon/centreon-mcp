from typing import ClassVar

from pydantic import BaseModel

from centreon_mcp.utils.mixins import ListMixin


class MonitoringServer(BaseModel, ListMixin):
    endpoint: ClassVar[str] = "monitoring/servers"

    id: int
    name: str
    address: str | None = None
    description: str | None = None
    is_running: bool
    last_alive: int | None = None
    version: str | None = None
