from typing import ClassVar

from pydantic import BaseModel

from centreon_mcp.utils.mixins import ListMixin


class HostGroup(BaseModel, ListMixin):
    endpoint: ClassVar[str] = "monitoring/hostgroups"

    id: int
    name: str
