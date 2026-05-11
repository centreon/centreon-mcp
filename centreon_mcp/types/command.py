from enum import IntEnum
from typing import ClassVar

from pydantic import BaseModel, Field

from centreon_mcp.types.base import CentreonBaseModel
from centreon_mcp.utils.request import request


class CommandType(IntEnum):
    NOTIFICATION = 1
    CHECK = 2
    MISCELLANEOUS = 3
    DISCOVERY = 4


class CommandArgument(BaseModel):
    name: str
    description: str


class CommandMacroType(IntEnum):
    HOST = 1
    SERVICE = 2


class CommandMacro(BaseModel):
    name: str
    type: CommandMacroType
    description: str


class CommandParams(BaseModel):
    name: str
    type: CommandType
    command_line: str
    is_shell: bool = Field(
        default=False,
        description=(
            "Is required if your command requires shell features like pipes, redirections, globbing etc."
            "If you are using the monitoring engine this option cannot be disabled."
            "Note that commands that require shell features are slowing down the poller server."
        ),
    )
    argument_example: str | None = Field(
        default=None, description="Example of command argument values"
    )
    arguments: list[CommandArgument] = Field(
        default_factory=list,
        description="descriptions of arguments used in the command line",
    )
    macros: list[CommandMacro] = Field(
        default_factory=list,
        description="descriptions of macros used in the command line",
    )
    connector_id: int | None = Field(
        default=None,
        description="A connector is run in the background and executes specific commands without the need to execute a binary.",
    )
    graph_template_id: int | None = Field(
        default=None, description="Graph template for the command"
    )


class Command(CentreonBaseModel):
    endpoint: ClassVar[str] = "configuration/commands"

    id: int
    name: str
    type: CommandType
    command_line: str
    is_activated: bool
    is_shell: bool
    is_locked: bool

    @staticmethod
    async def add(params: CommandParams) -> None:
        """
        Add a command.
        """
        payload = params.model_dump(mode="json")
        await request("POST", "configuration/commands", payload=payload)
