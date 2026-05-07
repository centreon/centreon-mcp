from typing import ClassVar

from centreon_mcp.types.base import CentreonBaseModel


class HostGroup(CentreonBaseModel):
    endpoint: ClassVar[str] = "monitoring/hostgroups"

    id: int
    name: str
