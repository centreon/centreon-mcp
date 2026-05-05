import json
from datetime import datetime
from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseFilter, BaseOrder
from centreon_mcp.utils.type import (
    Resource,
    ResourceStatus,
    ResourceType,
    StatusType,
    TimelineEvent,
    TimelineEventType,
    TimelineResource,
)

resource = FastMCP()


class ResourceOrder(BaseOrder):
    field: Literal["host.name", "host.alias", "host.address", "host.state"] = (
        "host.name"
    )


class ResourceFilter(BaseFilter):
    # Fields available for filtering in Centreon API
    name: str | None = Field(
        None,
        serialization_alias="name $lk",
        description="Name of the resource (host or service)",
    )
    alias: str | None = Field(
        None,
        serialization_alias="alias $lk",
        description="Alias of the resource (host or service)",
    )
    parent_name: str | None = Field(
        None,
        serialization_alias="parent_name $lk",
        description="Name of the parent resource (host or service)",
    )
    information_like: str | None = Field(
        None,
        serialization_alias="information $lk",
        description="Filter resources whose output/information contains this string (case-insensitive substring match)",
    )
    information_unlike: str | None = Field(
        None,
        serialization_alias="information $nk",
        description="Filter resources whose output/information does not contain this string (case-insensitive substring exclusion)",
    )


@resource.tool(
    annotations={
        "title": "List resources (hosts and services) in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_resources(
    filters: list[ResourceFilter] | None = None,
    types: list[ResourceType] | None = None,
    statuses: list[ResourceStatus] | None = None,
    hostgroup_names: list[str] | None = None,
    servicegroup_names: list[str] | None = None,
    host_category_names: list[str] | None = None,
    service_category_names: list[str] | None = None,
    monitoring_server_names: list[str] | None = None,
    status_types: list[StatusType] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: ResourceOrder | None = None,
) -> list[Resource]:
    """
    List resources (hosts and services) in real-time monitoring matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all resources except if explicitly intended.
    """
    logger.info("Executing tool list_resources")
    order = order or ResourceOrder()
    return await Resource.list(
        search=json.dumps(ResourceFilter.join(filters)),
        types=json.dumps(types or []),
        statuses=json.dumps(statuses or []),
        hostgroup_names=json.dumps(hostgroup_names or []),
        servicegroup_names=json.dumps(servicegroup_names or []),
        host_category_names=json.dumps(host_category_names or []),
        service_category_names=json.dumps(service_category_names or []),
        monitoring_server_names=json.dumps(monitoring_server_names or []),
        status_types=json.dumps(status_types or []),
        limit=limit,
        page=page,
        sort_by=order.model_dump_json(),
    )


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
    content_contains: str | None = Field(
        None,
        serialization_alias="content $lk",
        description="Substring match on the event content (case-insensitive).",
    )
    date_from: datetime | None = Field(
        None,
        serialization_alias="date $ge",
        description="Only return events whose date is greater than or equal to this ISO8601 datetime.",
    )
    date_to: datetime | None = Field(
        None,
        serialization_alias="date $le",
        description="Only return events whose date is less than or equal to this ISO8601 datetime.",
    )


@resource.tool(
    annotations={
        "title": "Get the event timeline of a resource (host or service) in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def get_resource_timeline(
    host_id: int,
    service_id: int | None
    filters: list[TimelineFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: TimelineOrder | None = None,
) -> list[TimelineEvent]:
    """
    Get the event timeline of a single resource (host or service) in real-time monitoring.
    Events include state changes, notifications, downtimes, acknowledgements and comments,
    each with a timestamp and content. Useful to answer "what happened recently on this
    resource ?" without leaving the conversation.
    Use tool `list_resources` first to get the host_id (and service_id if resource is a service).
    Results are sorted by date descending by default (most recent first).
    """
    logger.info("Executing tool get_resource_timeline")
    order = order or TimelineOrder()
    search = json.dumps(TimelineFilter.join(filters))
    sort_by = order.model_dump_json()
    if service_id is None:
      return await TimelineEvent.list_for_host(host_id, search, limit, page, sort_by)
    else:
      return await TimelineEvent.list_for_service(host_id, service_id, search, limit, page, sort_by)
