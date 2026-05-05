from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel

from centreon_mcp.types.base import BaseResource, CentreonBaseModel
from centreon_mcp.utils.request import request


class DowntimeParams(BaseModel):
    start_time: datetime
    end_time: datetime
    is_fixed: bool
    duration: int
    comment: str
    with_services: bool


class DowntimeResource(BaseResource):
    pass


class Downtime(CentreonBaseModel):
    endpoint: ClassVar[str] = "monitoring/downtimes"

    id: int
    author_id: int
    author_name: str
    host_id: int
    service_id: int | None
    poller_id: int
    comment: str
    duration: int | None
    entry_time: datetime | None
    start_time: datetime | None
    end_time: datetime | None
    deletion_time: datetime | None
    actual_start_time: datetime | None
    actual_end_time: datetime | None
    is_started: bool
    is_fixed: bool
    is_cancelled: bool

    @classmethod
    async def set(cls, params: DowntimeParams, resources: list[DowntimeResource]) -> None:
        """
        Set a downtime on multiple resources.
        """
        payload = {
            "downtime": params.model_dump(mode="json"),
            "resources": [resource.dump() for resource in resources],
        }
        await request("POST", "monitoring/resources/downtime", payload=payload)

    @staticmethod
    async def cancel(downtime_id: int) -> None:
        """
        Cancel a downtime.
        """
        await request("DELETE", f"monitoring/downtimes/{downtime_id}")
