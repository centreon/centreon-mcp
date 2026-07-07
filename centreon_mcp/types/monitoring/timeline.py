from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder, Status
from centreon_mcp.utils.request import request

TimelineEventType = Literal["event", "notification", "downtime", "acknowledgement", "comment"]


class TimelineOrder(BaseOrder):
    field: Literal["date", "type", "content"] = "date"
    order: Literal["ASC", "DESC"] = "DESC"


class TimelineFilter(BaseFilter):
    event_type: TimelineEventType | None = Field(
        None,
        serialization_alias="type $eq",
        description=(
            "Restrict to a single event type (event, notification, downtime, "
            "acknowledgement, comment)."
        ),
    )
    start_date: datetime | None = Field(
        None,
        serialization_alias="date $ge",
        description="Only return events whose date is greater than or equal to this ISO8601 datetime.",
    )
    end_date: datetime | None = Field(
        None,
        serialization_alias="date $le",
        description="Only return events whose date is less than or equal to this ISO8601 datetime.",
    )


class TimelineContact(BaseModel):
    id: int | None = None
    name: str | None = None


class TimelineEvent(BaseModel):
    id: int
    type: TimelineEventType
    date: datetime
    start_date: datetime | None = None
    end_date: datetime | None = None
    content: str
    contact: TimelineContact | None = None
    status: Status | None = None
    tries: int | None = None

    @staticmethod
    async def _list(
        endpoint: str,
        search: str | None = None,
        limit: int | None = None,
        page: int | None = None,
        sort_by: str | None = None,
    ) -> list["TimelineEvent"]:
        """
        Internal method to list timeline events for a resource.
        """
        params = {"search": search, "limit": limit, "page": page, "sort_by": sort_by}
        content = await request("GET", endpoint, params=params)
        return [TimelineEvent(**item) for item in content["result"]]

    @staticmethod
    async def list_for_host(
        host_id: int,
        search: str | None = None,
        limit: int | None = None,
        page: int | None = None,
        sort_by: str | None = None,
    ) -> list["TimelineEvent"]:
        """
        List timeline events for a host.
        """
        endpoint = f"monitoring/hosts/{host_id}/timeline"
        return await TimelineEvent._list(endpoint, search, limit, page, sort_by)

    @staticmethod
    async def list_for_service(
        host_id: int,
        service_id: int,
        search: str | None = None,
        limit: int | None = None,
        page: int | None = None,
        sort_by: str | None = None,
    ) -> list["TimelineEvent"]:
        """
        List timeline events for a service.
        """
        endpoint = f"monitoring/hosts/{host_id}/services/{service_id}/timeline"
        return await TimelineEvent._list(endpoint, search, limit, page, sort_by)
