import asyncio

from fastmcp import FastMCP

from centreon_mcp.types.configuration.monitoring_server import (
    MonitoringServerConfiguration,
)
from centreon_mcp.utils import logger

monitoring_server = FastMCP()


@monitoring_server.tool(
    annotations={
        "title": "Generate monitoring servers configurations",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def generate_monitoring_servers_configurations(
    monitoring_servers_ids: list[int] | None = None,
) -> bool | dict[int, bool | BaseException]:
    """
    Generate configurations of monitoring servers based on their ids.
    If no ids provided, generate configurations of all monitoring servers.
    """
    logger.info("Executing tool generate_monitoring_servers_configurations")

    # If no ids, generate all configurations
    if monitoring_servers_ids is None:
        return await MonitoringServerConfiguration.generate()

    # Else, generate configurations concurrently
    tasks = [
        asyncio.create_task(MonitoringServerConfiguration.generate(monitoring_server_id))
        for monitoring_server_id in monitoring_servers_ids
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return dict(zip(monitoring_servers_ids, results, strict=True))


@monitoring_server.tool(
    annotations={
        "title": "Reload monitoring servers configurations",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def reload_monitoring_servers_configurations(
    monitoring_servers_ids: list[int] | None = None,
) -> bool | dict[int, bool | BaseException]:
    """
    Reload configurations of monitoring servers based on their ids.
    If no ids provided, reload configurations of all monitoring servers.
    """
    logger.info("Executing tool reload_monitoring_servers_configurations")

    # If no ids, reload all configurations
    if monitoring_servers_ids is None:
        return await MonitoringServerConfiguration.reload()

    # Else, reload configurations concurrently
    tasks = [
        asyncio.create_task(MonitoringServerConfiguration.reload(monitoring_server_id))
        for monitoring_server_id in monitoring_servers_ids
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return dict(zip(monitoring_servers_ids, results, strict=True))
