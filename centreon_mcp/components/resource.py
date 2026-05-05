import json
from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseFilter, BaseOrder
from centreon_mcp.utils.type import (
    Check,
    CheckResource,
    Resource,
    ResourceStatus,
    ResourceType,
    StatusType,
)


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


@resource.tool(
    annotations={
        "title": "Request a check on resources (hosts and services) in real-time monitoring",
        "readOnlyHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def request_check(
    resources: list[CheckResource],
    is_forced: Annotated[
        bool,
        Field(
            description=(
                "If true, the check is executed immediately, bypassing the configured "
                "check interval. If false, the check is scheduled at the next available "
                "execution slot. Defaults to true."
            ),
        ),
    ] = True,
) -> bool:
    """
    Trigger a check on multiple resources (hosts and services) in real-time monitoring.
    Useful to refresh state on demand without waiting for the next polling cycle —
    for example, right after a remediation action.
    Use tool `list_resources` first to get the resource IDs.
    """
    logger.info("Executing tool request_check")
    await Check.request(is_forced, resources)
    return True
