from datetime import datetime
from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder, BaseResource, HostState
from centreon_mcp.utils.mixins import DeleteMixin, ListMixin
from centreon_mcp.utils.request import request


class DowntimeOrder(BaseOrder):
    field: Literal[
        "id",
        "host.id",
        "host.name",
        "host.alias",
        "host.address",
        "host.state",
        "start_time",
        "end_time",
        "entry_time",
        "deletion_time",
    ] = "id"


class DowntimeFilter(BaseFilter):
    host_id: int | None = Field(None, serialization_alias="host.id $eq")
    host_name: str | None = Field(None, serialization_alias="host.name $eq")
    host_alias: str | None = Field(None, serialization_alias="host.alias $eq")
    host_address: str | None = Field(None, serialization_alias="host.address $eq")
    host_state: HostState | None = Field(None, serialization_alias="host.state $eq")
    is_fixed: bool | None = Field(None, serialization_alias="is_fixed $eq")
    is_cancelled: bool | None = Field(None, serialization_alias="is_cancelled $eq")
    poller_id: int | None = Field(None, serialization_alias="poller.id $eq")


class DowntimeParams(BaseModel):
    start_time: datetime
    end_time: datetime
    is_fixed: bool
    duration: int
    comment: str
    with_services: bool


class DowntimeResource(BaseResource):
    pass


class Downtime(BaseModel, ListMixin[DowntimeFilter, DowntimeOrder], DeleteMixin):
    endpoint: ClassVar[str] = "monitoring/downtimes"

    id: int
    author_id: int
    author_name: str
    host_id: int
    service_id: int | None = None
    poller_id: int
    comment: str
    duration: int | None = None
    entry_time: datetime | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    deletion_time: datetime | None = None
    actual_start_time: datetime | None = None
    actual_end_time: datetime | None = None
    is_started: bool
    is_fixed: bool
    is_cancelled: bool

    @classmethod
    async def set(cls, params: DowntimeParams, resources: list[DowntimeResource]) -> bool:
        """
        Set a downtime on multiple resources.
        Return True if successful; otherwise, raise an exception.
        """
        payload = {
            "downtime": params.model_dump(mode="json"),
            "resources": [resource.dump() for resource in resources],
        }
        await request("POST", "monitoring/resources/downtime", payload=payload)
        return True
