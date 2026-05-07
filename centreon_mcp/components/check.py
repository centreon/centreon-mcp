from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.types.check import Check, CheckResource
from centreon_mcp.utils import logger

check = FastMCP()


@check.tool(
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
