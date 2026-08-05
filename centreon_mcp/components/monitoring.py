import json
from collections.abc import Sequence
from typing import Annotated, Literal, cast

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.types.monitoring import Monitoring, MonitoringFilter, MonitoringOrder
from centreon_mcp.types.monitoring.actions import (
    MonitoringAction,
    MonitoringActionFilter,
    MonitoringActionOrder,
    MonitoringActionParams,
)
from centreon_mcp.types.monitoring.mapping import (
    MODELS_MIXIN_COUNT,
    MODELS_MIXIN_DELETE,
    MODELS_MIXIN_LIST,
    MODELS_MIXIN_SET,
)
from centreon_mcp.types.monitoring.resource import Resource, ResourceFilter, ResourceOrder
from centreon_mcp.types.monitoring.status import ResourceStatusCount, ResourceStatusCountFilter
from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseResource, ResourceStatus, ResourceType, StatusType

monitoring = FastMCP()


@monitoring.tool(
    annotations={
        "title": "List resources (hosts and services) in real-time monitoring",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_monitoring_resources(
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
    If no filters are provided, ask users to provide at least one filter,
    unless retrieving all resources is explicitly intended.
    """
    logger.info("Executing tool list_monitoring_resources")
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
    return await Resource.list(filters, limit, page, order, extras)


@monitoring.tool(
    annotations={
        "title": "List monitoring entities",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_monitoring_entities(
    model_type: Literal[
        "host_group",
        "service_group",
        "monitoring_server",
    ],
    filters: Sequence[MonitoringFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: MonitoringOrder | None = None,
) -> list[Monitoring]:
    """
    List real-time monitoring entities matching the given filters.
    The entities kind is selected via model_type:
        - Host Groups
        - Service Groups
        - Monitoring Servers
    If no filters are provided, ask users to provide at least one filter,
    unless retrieving all entities is explicitly intended.
    """
    logger.info("Executing tool list_monitoring")

    # Check compatibility between model and order types
    if order is not None:
        order.check(model_type)

    # Check compatibility between model and filters types
    if filters is not None:
        [f.check(model_type) for f in filters]

    models = await MODELS_MIXIN_LIST[model_type].list(filters, limit, page, order)
    return cast(list[Monitoring], models)


@monitoring.tool(
    annotations={
        "title": "List monitoring actions",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_monitoring_actions(
    model_type: Literal["acknowledgement", "downtime"],
    filters: Sequence[MonitoringActionFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: MonitoringActionOrder | None = None,
) -> list[MonitoringAction]:
    """
    List real-time monitoring actions matching the given filters.
    The action kind is selected via model_type:
        - Acknowledgements
        - Downtimes
    If no filters are provided, ask users to provide at least one filter,
    unless retrieving all entities is explicitly intended.
    """
    logger.info("Executing tool list_monitoring_actions")

    # Check compatibility between model and order types
    if order is not None:
        order.check(model_type)

    # Check compatibility between model and filters types
    if filters is not None:
        [f.check(model_type) for f in filters]

    models = await MODELS_MIXIN_LIST[model_type].list(filters, limit, page, order)
    return cast(list[MonitoringAction], models)


@monitoring.tool(
    annotations={
        "title": "Set monitoring actions",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def set_monitoring_actions(
    model_type: Literal["acknowledgement", "downtime", "comment", "check"],
    params: MonitoringActionParams,
    resources: list[BaseResource],
) -> bool:
    """
    Set a real-time monitoring actions on selected resources.
    The action kind is selected via model_type:
        - Acknowledgement
        - Downtime
        - Check
        - Comment
    """
    logger.info("Executing tool set_monitoring_actions")

    # Check compatibility between model and params types
    params.check(model_type)

    return await MODELS_MIXIN_SET[model_type].set(params, resources)


@monitoring.tool(
    annotations={
        "title": "Cancel monitoring actions",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def cancel_monitoring_actions(
    model_type: Literal["acknowledgement", "downtime"],
    model_ids: list[int],
) -> dict[int, bool | BaseException]:
    """
    Cancel real-time monitoring actions  from their ids.
    The action kind is selected via model_type:
        - Acknowledgement
        - Downtime
    """
    logger.info("Executing tool cancel_monitoring_actions")
    return await MODELS_MIXIN_DELETE[model_type].delete(model_ids)


@monitoring.tool(
    annotations={
        "title": "Count resources by status in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def count_monitoring_resources_by_status(
    model_type: Literal["host", "service"],
    filters: Sequence[ResourceStatusCountFilter] | None = None,
) -> ResourceStatusCount:
    """
    Count resources (host/service) by status in real-time monitoring matching given filters.
    If no filters are provided, ask users to provide at least one filter,
    unless counting all resources statuses is explicitly intended.
    Use this tool instead of list_monitoring_resources when only aggregate counts are needed.
    """
    logger.info("Executing tool count_monitoring_resources_by_status")

    # Check compatibility between model and filters types
    if filters is not None:
        [f.check(model_type) for f in filters]

    count = await MODELS_MIXIN_COUNT[model_type].count(filters)
    return cast(ResourceStatusCount, count)
