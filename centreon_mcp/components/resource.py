import json
from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.components.base import _list
from centreon_mcp.types.base import ResourceType, StatusType
from centreon_mcp.types.resource import Resource, ResourceStatus
from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseFilter, BaseOrder

resource = FastMCP()


class ResourceOrder(BaseOrder):
    field: Literal["host.name", "host.alias", "host.address", "host.state"] = "host.name"


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
        "destructiveHint": False,
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
    fields = {
        "types": types,
        "statuses": statuses,
        "hostgroup_names": hostgroup_names,
        "servicegroup_names": servicegroup_names,
        "host_category_names": host_category_names,
        "service_category_names": service_category_names,
        "monitoring_server_names": monitoring_server_names,
        "status_types": status_types,
    }
    extras = {name: json.dumps(value) for name, value in fields.items() if value}
    return await _list(Resource, filters, limit, page, order, extras)
