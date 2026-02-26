import asyncio
import json
from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder
from centreon_mcp.utils.type import Resource, ResourceStatus, ResourceType, StatusType

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
    limit: Annotated[int, Field(ge=1)] = 10,
    page: Annotated[int, Field(ge=1)] = 1,
    order: ResourceOrder | None = None,
) -> list[Resource]:
    """
    List resources (hosts and services) in real-time monitoring matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all resources except if explicitly intended.
    """
    filters = filters or []
    order = order or ResourceOrder()
    await asyncio.gather(*(filter.complete() for filter in filters))
    conditions = (
        {
            "$or": [
                {"$and": filter.conditions} for filter in filters if filter.conditions
            ]
        }
        if filters
        else {}
    )
    sort_by = order.model_dump_json()
    return await Resource.list(
        search=json.dumps(conditions),
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
        sort_by=sort_by,
    )
