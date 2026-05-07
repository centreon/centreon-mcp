from typing import ClassVar

from centreon_mcp.types.base import CentreonBaseModel


class ServiceGroup(CentreonBaseModel):
    endpoint: ClassVar[str] = "monitoring/servicegroups"

    id: int
    name: str
