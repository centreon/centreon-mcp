from fastmcp import FastMCP

from centreon_mcp.types.monitoring.check import Check, CheckParams, CheckResource
from centreon_mcp.utils import logger

check = FastMCP()


@check.tool(
    annotations={
        "title": "Request a check on resources (hosts and services) in real-time monitoring",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def request_check(resources: list[CheckResource], params: CheckParams) -> bool:
    """
    Trigger a check on multiple resources (hosts and services) in real-time monitoring.
    Useful to refresh state on demand without waiting for the next polling cycle —
    for example, right after a remediation action.
    Use tool `list_resources` first to get the resource IDs.
    """
    logger.info("Executing tool request_check")
    return await Check.request(params, resources)
