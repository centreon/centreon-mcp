from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.components.base import _list
from centreon_mcp.types.monitoring_server import MonitoringServer, MonitoringServerConfiguration
from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseFilter, BaseOrder

monitoring_server = FastMCP()


class MonitoringServerOrder(BaseOrder):
    field: Literal["id", "name", "running"] = "name"


class MonitoringServerFilter(BaseFilter):
    monitoring_server_id: int | None = Field(None, serialization_alias="id $eq")
    monitoring_server_name: str | None = Field(None, serialization_alias="name $eq")
    monitoring_server_running: bool | None = Field(None, serialization_alias="running $eq")


@monitoring_server.tool(
    annotations={
        "title": "List monitoring servers in real-time monitoring",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_monitoring_servers(
    filters: list[MonitoringServerFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: MonitoringServerOrder | None = None,
) -> list[MonitoringServer]:
    """
    List monitoring servers in real-time monitoring matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all monitoring servers except if explicitly intended.
    """
    logger.info("Executing tool list_monitoring_servers")
    return await _list(MonitoringServer, filters, limit, page, order)


class MonitoringServerConfigurationOrder(BaseOrder):
    field: Literal["id", "name"] = "name"


class MonitoringServerConfigurationFilter(BaseFilter):
    monitoring_server_id: int | None = Field(None, serialization_alias="id $eq")
    monitoring_server_name: str | None = Field(None, serialization_alias="name $eq")


@monitoring_server.tool(
    annotations={
        "title": "List monitoring servers configurations",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_monitoring_servers_configurations(
    filters: list[MonitoringServerConfigurationFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: MonitoringServerConfigurationOrder | None = None,
) -> list[MonitoringServerConfiguration]:
    """
    List monitoring servers configurations matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all monitoring servers configurations except if explicitly intended.
    """
    logger.info("Executing tool list_monitoring_servers_configurations")
    return await _list(MonitoringServerConfiguration, filters, limit, page, order)
