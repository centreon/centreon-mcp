from typing import ClassVar

from pydantic import BaseModel

from centreon_mcp.utils.mixins import ListMixin


class MonitoringServer(ListMixin, BaseModel):
    endpoint: ClassVar[str] = "monitoring/servers"

    id: int
    name: str
    address: str | None
    description: str | None = None
    is_running: bool
    last_alive: int | None
    version: str | None
