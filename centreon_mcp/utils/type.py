from enum import Enum
from typing import ClassVar, Type, TypeVar

from pydantic import BaseModel

from centreon_mcp.utils.request import request

T = TypeVar("T", bound="CentreonBaseModel")


class CentreonBaseModel(BaseModel):
    endpoint: ClassVar[str]

    @classmethod
    async def list(
        cls: Type[T],
        search: str | None = None,
        limit: int | None = None,
        page: int | None = None,
        sort_by: str | None = None,
    ) -> list[T]:
        """
        List resource of type T in real-time monitoring matching the search string.
        """
        params = {"search": search, "limit": limit, "page": page, "sort_by": sort_by}
        params = {name: value for name, value in params.items() if value is not None}
        content = await request("GET", cls.endpoint, params=params)
        return [cls(**item) for item in content["result"]]


class HostState(int, Enum):
    UP = 0
    DOWN = 1
    UNREACHABLE = 2
    PENDING = 4


class Host(CentreonBaseModel):
    endpoint: ClassVar[str] = "monitoring/hosts"

    id: int
    name: str
    alias: str
    address_ip: str
    state: HostState
    poller_id: int
    acknowledged: bool


class ServiceState(int, Enum):
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3
    PENDING = 4


class Service(CentreonBaseModel):
    endpoint: ClassVar[str] = "monitoring/services"

    id: int
    description: str
    display_name: str
    state: ServiceState


class HostGroup(CentreonBaseModel):
    endpoint: ClassVar[str] = "monitoring/hostgroups"

    id: int
    name: str


class ServiceGroup(CentreonBaseModel):
    endpoint: ClassVar[str] = "monitoring/servicegroups"

    id: int
    name: str
