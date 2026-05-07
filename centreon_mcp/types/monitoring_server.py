from typing import ClassVar

from centreon_mcp.types.base import CentreonBaseModel


class MonitoringServer(CentreonBaseModel):
    endpoint: ClassVar[str] = "monitoring/servers"

    id: int
    name: str
    address: str | None
    description: str | None = None
    is_running: bool
    last_alive: int | None
    version: str | None
