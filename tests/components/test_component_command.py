from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.command import (
    CommandFilter,
    CommandOrder,
    add_command,
    list_commands,
)
from centreon_mcp.types.configuration.command import Command, CommandParams

MODULE = "centreon_mcp.components.command"


@patch(f"{MODULE}._list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_commands(logger: MagicMock, _list: AsyncMock):

    # Setup args
    filters = [CommandFilter.model_construct()]
    limit = 50
    page = 1
    order = CommandOrder()

    # Mock logger
    logger.debug.return_value = None

    # Mock _list
    command = Command.model_construct()
    _list.return_value = [command]

    # Call test function
    results = await list_commands(filters, limit, page, order)

    # Assert _list called with right args
    _list.assert_awaited_once_with(Command, filters, limit, page, order)

    # Assert result
    assert results[0] == command


@patch(f"{MODULE}.Command.add", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_add_command(logger: MagicMock, command_add: AsyncMock):

    # Setup args
    params = CommandParams.model_construct()

    # Mock logger
    logger.info.return_value = None

    # Mock Command.add
    command_add.return_value = True

    # Call test function
    result = await add_command(params)

    # Assert Command.add called with right args
    command_add.assert_awaited_once_with(params)

    # Assert result
    assert result
