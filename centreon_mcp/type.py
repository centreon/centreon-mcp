from enum import Enum

from pydantic import BaseModel

from centreon_mcp.utils.request import request


class HostState(int, Enum):
    UP = 0
    DOWN = 1
    UNREACHABLE = 2
    PENDING = 4


class Host(BaseModel):
    id: int
    name: str
    alias: str
    address_ip: str
    state: HostState
    poller_id: int
    acknowledged: bool

    @classmethod
    async def list(
        cls, search: str, limit: int, page: int, sort_by: str
    ) -> list["Host"]:
        """
        List hosts matching the search string.
        """
        params = {"search": search, "limit": limit, "page": page, "sort_by": sort_by}
        content = await request("GET", "monitoring/hosts", params=params)
        return [cls(**item) for item in content["result"]]


class ServiceState(int, Enum):
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3
    PENDING = 4


class Service(BaseModel):
    id: int
    description: str
    display_name: str
    state: ServiceState

    @classmethod
    async def list(
        cls, search: str, limit: int, page: int, sort_by: str
    ) -> list["Service"]:
        """
        List all services.
        """
        params = {"search": search, "limit": limit, "page": page, "sort_by": sort_by}
        content = await request("GET", "monitoring/services", params=params)
        return [cls(**item) for item in content["result"]]
