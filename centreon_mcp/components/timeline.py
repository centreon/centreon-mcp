import json
from datetime import datetime
from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.types.timeline import TimelineEvent, TimelineEventType
from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseFilter, BaseOrder

timeline = FastMCP()


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


@timeline.tool(
    annotations={
        "title": "Get the event timeline of a host in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def get_host_timeline(
    host_id: int,
    filters: list[TimelineFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: TimelineOrder | None = None,
) -> list[TimelineEvent]:
    """
    Get the event timeline of a single host in real-time monitoring.
    Events include state changes, notifications, downtimes, acknowledgements and comments,
    each with a timestamp and content. Useful to answer "what happened recently on this
    resource ?" without leaving the conversation.
    Use tool `list_resources` first to get the host_id
    Results are sorted by date descending by default (most recent first).
    """
    logger.info("Executing tool get_host_timeline")
    order = order or TimelineOrder()
    return await TimelineEvent.list_for_host(
        host_id,
        search=json.dumps(TimelineFilter.join(filters)),
        limit=limit,
        page=page,
        sort_by=order.model_dump_json(),
    )


@timeline.tool(
    annotations={
        "title": "Get the event timeline of a service in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def get_service_timeline(
    host_id: int,
    service_id: int,
    filters: list[TimelineFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: TimelineOrder | None = None,
) -> list[TimelineEvent]:
    """
    Get the event timeline of a single service in real-time monitoring.
    Events include state changes, notifications, downtimes, acknowledgements and comments,
    each with a timestamp and content. Useful to answer "what happened recently on this
    resource ?" without leaving the conversation.
    Use tool `list_resources` first to get the host_id and service_id.
    Results are sorted by date descending by default (most recent first).
    """
    logger.info("Executing tool get_service_timeline")
    order = order or TimelineOrder()
    return await TimelineEvent.list_for_service(
        host_id,
        service_id,
        search=json.dumps(TimelineFilter.join(filters)),
        limit=limit,
        page=page,
        sort_by=order.model_dump_json(),
    )
