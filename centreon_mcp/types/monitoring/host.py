from pydantic import BaseModel

from centreon_mcp.types.base import StatusCount
from centreon_mcp.utils.request import request


class HostStatusCount(StatusCount):
    up: int
    down: int
    unreachable: int


class Host(BaseModel):
    @staticmethod
    async def count_by_status(search: str | None) -> HostStatusCount:
        """
        Count hosts by status.
        """
        params = {"search": search}
        content = await request("GET", "monitoring/hosts/status", params=params)
        return HostStatusCount(**content)
