import json
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.types.monitoring.timeline import TimelineEvent, TimelineFilter, TimelineOrder
from centreon_mcp.utils import logger

timeline = FastMCP()


@timeline.tool(
    annotations={
        "title": "Get the event timeline of a host in real-time monitoring",
        "readOnlyHint": True,
        "destructiveHint": False,
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
        sort_by=order.model_dump_json(exclude={"model_type"}),
    )


@timeline.tool(
    annotations={
        "title": "Get the event timeline of a service in real-time monitoring",
        "readOnlyHint": True,
        "destructiveHint": False,
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
        sort_by=order.model_dump_json(exclude={"model_type"}),
    )
