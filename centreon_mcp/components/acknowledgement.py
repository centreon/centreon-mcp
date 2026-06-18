from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.components.base import _list
from centreon_mcp.types.monitoring.acknowledgement import (
    Acknowledgement,
    AcknowledgementFilter,
    AcknowledgementOrder,
    AcknowledgementParams,
    AcknowledgementResource,
)
from centreon_mcp.utils import logger

acknowledgement = FastMCP()


@acknowledgement.tool(
    annotations={
        "title": "List all acknowledgements in real-time monitoring",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_acknowledgements(
    filters: list[AcknowledgementFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: AcknowledgementOrder | None = None,
) -> list[Acknowledgement]:
    """
    List all acknowledgements in real-time monitoring.
    """
    logger.info("Executing tool list_acknowledgements")
    return await _list(Acknowledgement, filters, limit, page, order)


@acknowledgement.tool(
    annotations={
        "title": "Add acknowledgement on multiple resources in real-time monitoring",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def add_acknowledgements(
    params: AcknowledgementParams,
    resources: list[AcknowledgementResource],
) -> bool:
    """
    Add an acknowledgement on multiple resources in real-time monitoring.
    Use tool `list_resources` first to get resources IDs.
    """
    logger.info("Executing tool add_acknowledgements")
    return await Acknowledgement.add(params, resources)


@acknowledgement.tool(
    annotations={
        "title": "Cancel acknowledgements on multiple resources in real-time monitoring",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def cancel_acknowledgements(
    with_services: Annotated[
        bool, "Whether to cancel services acknowledgements if host is acknowledged"
    ],
    resources: list[AcknowledgementResource],
) -> bool:
    """
    Cancel acknowledgements on multiple resources in real-time monitoring.
    Use tool `list_acknowledgements` first to get acknowledged resources IDs.
    """
    logger.info("Executing tool cancel_acknowledgements")
    return await Acknowledgement.cancel(with_services, resources)
