from enum import IntEnum
from typing import Literal

from pydantic import BaseModel

from centreon_mcp.types.base import StatusCount
from centreon_mcp.utils.request import request

HostStatus = Literal["UP", "DOWN", "UNREACHABLE", "PENDING"]


class HostState(IntEnum):
    UP = 0
    DOWN = 1
    UNREACHABLE = 2
    PENDING = 4


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
