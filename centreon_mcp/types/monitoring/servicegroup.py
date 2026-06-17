from typing import ClassVar

from pydantic import BaseModel

from centreon_mcp.utils.mixins import ListMixin


class ServiceGroup(BaseModel, ListMixin):
    endpoint: ClassVar[str] = "monitoring/servicegroups"

    id: int
    name: str
