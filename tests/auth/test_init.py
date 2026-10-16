from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from centreon_mcp.auth import ENTRY_POINTS_GROUP, Role, load, require_roles
from centreon_mcp.auth.models import AuthenticationError

MODULE = "centreon_mcp.auth"


@pytest.fixture
def plugins() -> list[MagicMock]:
    mocks = []
    for name in ["first", "second"]:
        # `name` is a reserved MagicMock constructor argument, so set the attribute afterwards
        mock = MagicMock()
        mock.name = name
        mocks.append(mock)
    return mocks


@patch(f"{MODULE}.plugin", create=True)
@patch(f"{MODULE}.entry_points")
@patch(f"{MODULE}.settings")
def test_load(settings: MagicMock, entry_points: MagicMock, _: MagicMock, plugins: list[MagicMock]):

    # Setup two registered plugins and select the second one
    entry_points.return_value = plugins
    settings.auth_plugin = "second"

    # Call test function
    load()

    # Assertions
    entry_points.assert_called_once_with(group=ENTRY_POINTS_GROUP)
    plugins[0].load.assert_not_called()
    plugins[1].load.assert_called_once_with()


@patch(f"{MODULE}.plugin", create=True)
@patch(f"{MODULE}.entry_points")
@patch(f"{MODULE}.settings")
def test_load_unknown(
    settings: MagicMock, entry_points: MagicMock, _: MagicMock, plugins: list[MagicMock]
):

    # Setup registered plugins not matching the selected one
    entry_points.return_value = plugins
    settings.auth_plugin = "unknown"

    # Call test function
    with pytest.raises(ValueError, match="Unknown authentication plugin 'unknown'") as error:
        load()

    # Assertions
    assert "Available plugins: first,second" in str(error.value)
    for plugin in plugins:
        plugin.load.assert_not_called()


@pytest.mark.parametrize(
    "role, expected",
    [
        (Role.NONE, False),
        (Role.READER, False),
        (Role.EDITOR, True),
        (Role.ADMIN, True),
    ],
)
@patch(f"{MODULE}.plugin", new_callable=MagicMock, create=True)
async def test_requires_role(plugin: MagicMock, role: Role, expected: bool):

    # Setup args
    level = Role.EDITOR
    context = MagicMock()

    # Mock plugin.role to return the user role
    plugin.role = AsyncMock(return_value=role)

    # Call test function
    check = require_roles(level)
    granted = await check(context)

    # Assertions
    assert granted is expected
    plugin.role.assert_awaited_once_with(context.token)


@patch(f"{MODULE}.logger")
@patch(f"{MODULE}.plugin", new_callable=MagicMock, create=True)
async def test_requires_role_authentication_error(plugin: MagicMock, logger: MagicMock):

    # Setup args
    level = Role.READER
    context = MagicMock()
    context.component.name = "list_configurations"

    # Mock plugin.role to refuse the user identity
    plugin.role = AsyncMock(side_effect=AuthenticationError("unknown user"))

    # Call test function
    check = require_roles(level)
    granted = await check(context)

    # Assertions
    assert granted is False
    plugin.role.assert_awaited_once_with(context.token)
    logger.info.assert_called_once_with("Denying list_configurations: unknown user")
