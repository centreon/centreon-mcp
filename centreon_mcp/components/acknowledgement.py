from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.types.acknowledgement import (
    Acknowledgement,
    AcknowledgementParams,
    AcknowledgementResource,
)
from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseFilter, BaseOrder, _list

acknowledgement = FastMCP()


class AcknowledgementOrder(BaseOrder):
    field: Literal[
        "id",
        "host.id",
        "host.name",
        "host.alias",
        "host.address",
        "host.state",
        "start_time",
        "end_time",
        "entry_time",
        "deletion_time",
    ] = "id"


class AcknowledgementFilter(BaseFilter):
    # Fields available for filtering in Centreon API
    pass


@acknowledgement.tool(
    annotations={
        "title": "List all acknowledgements in real-time monitoring",
        "readOnlyHint": True,
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
    return await _list(Acknowledgement, AcknowledgementOrder, filters, limit, page, order)


@acknowledgement.tool(
    annotations={
        "title": "Add acknowledgement on multiple resources in real-time monitoring",
        "readOnlyHint": False,
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
