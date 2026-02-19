from typing import Annotated, List

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.utils.type import HostAcknowledgement, ServiceAcknowledgement

acknowledgement = FastMCP()


@acknowledgement.tool(
    annotations={
        "title": "List all hosts acknowledgements in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_host_acknowledgements(
    limit: Annotated[int, Field(ge=1)] = 10,
    page: Annotated[int, Field(ge=1)] = 1,
) -> List[HostAcknowledgement]:
    """
    List all hosts acknowledgements in real-time monitoring.
    """
    return await HostAcknowledgement.list(limit=limit, page=page)


@acknowledgement.tool(
    annotations={
        "title": "List all services acknowledgements in real-time monitoring",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_service_acknowledgements(
    limit: Annotated[int, Field(ge=1)] = 10,
    page: Annotated[int, Field(ge=1)] = 1,
) -> List[ServiceAcknowledgement]:
    """
    List all services acknowledgements in real-time monitoring.
    """
    return await ServiceAcknowledgement.list(limit=limit, page=page)
