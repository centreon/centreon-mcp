from unittest.mock import AsyncMock, patch

from centreon_mcp.types.configuration.command import Command, CommandParams

MODULE = "centreon_mcp.types.configuration.command"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_add_command(request: AsyncMock):

    # Setup args
    params = CommandParams.model_construct()

    # Mock request
    request.return_value = None

    # Call test function
    await Command.add(params)

    # Assert request called with right args
    payload = params.model_dump(mode="json")
    request.assert_awaited_once_with("POST", "configuration/commands", payload=payload)
