from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from centreon_mcp.components.base import _list
from centreon_mcp.types.command import Command, CommandParams, CommandType
from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseFilter, BaseOrder

command = FastMCP()


class CommandOrder(BaseOrder):
    field: Literal["name"] = "name"


class CommandFilter(BaseFilter):
    command_id: int | None = Field(None, serialization_alias="id $eq")
    command_name: str | None = Field(None, serialization_alias="name $eq")
    command_type: CommandType | None = Field(None, serialization_alias="type $eq")
    command_is_locked: bool | None = Field(None, serialization_alias="is_locked $eq")


@command.tool(
    annotations={
        "title": "List commands",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def list_commands(
    filters: list[CommandFilter] | None = None,
    limit: Annotated[int, Field(ge=1)] = 50,
    page: Annotated[int, Field(ge=1)] = 1,
    order: CommandOrder | None = None,
) -> list[Command]:
    """
    List commands matching the given filters.
    If no filters are provided, ask users to provide at least one filter
    to avoid retrieving all commands except if explicitly intended.
    """
    logger.info("Executing tool list_commands")
    return await _list(Command, filters, limit, page, order)


@command.tool(
    annotations={
        "title": "Add a command",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def add_command(params: CommandParams) -> bool:
    """
    Add a command.
    """
    logger.info("Executing tool add_command")
    return await Command.add(params)
