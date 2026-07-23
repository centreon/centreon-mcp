from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.types.monitoring.actions.acknowledgement import (
    Acknowledgement,
    AcknowledgementFilter,
    AcknowledgementOrder,
    AcknowledgementParams,
)
from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseResource

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
    return await Acknowledgement.list(filters, limit, page, order)


@acknowledgement.tool(
    annotations={
        "title": "Set acknowledgement on multiple resources in real-time monitoring",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def set_acknowledgements(
    params: AcknowledgementParams,
    resources: list[BaseResource],
) -> bool:
    """
    Create an acknowledgement on multiple resources in real-time monitoring.
    Use tool `list_resources` first to get resources IDs.
    """
    logger.info("Executing tool set_acknowledgements")
    return await Acknowledgement.set(params, resources)


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
    resources: list[BaseResource],
) -> bool:
    """
    Cancel acknowledgements on multiple resources in real-time monitoring.
    Use tool `list_acknowledgements` first to get acknowledged resources IDs.
    """
    logger.info("Executing tool cancel_acknowledgements")
    return await Acknowledgement.cancel(with_services, resources)
