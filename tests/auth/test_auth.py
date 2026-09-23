from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from centreon_mcp.auth import (
    BUILT_IN_PLUGINS,
    ENTRY_POINT_GROUP,
    Role,
    load_plugin,
    require_role,
)
from centreon_mcp.auth.base import AuthPlugin
from centreon_mcp.auth.none import NoAuthPlugin

MODULE = "centreon_mcp.auth"


def stub() -> MagicMock:
    """
    Mock a plugin that satisfies the contract, which a bare mock does not.
    """
    return MagicMock(spec=AuthPlugin)


@pytest.mark.parametrize("name", sorted(BUILT_IN_PLUGINS))
async def test_load_plugin_built_in(name: str):

    # Call test function: built-in plugins resolve without relying on package metadata
    with patch(f"{MODULE}.import_plugin", new_callable=MagicMock) as import_plugin:
        import_plugin.return_value = stub()
        plugin = load_plugin(name)

    # Assert the declared implementation was imported
    import_plugin.assert_called_once_with(BUILT_IN_PLUGINS[name])
    assert plugin == import_plugin.return_value


async def test_load_plugin_entry_point():

    # Mock an entry point published by a third party package
    entry_point = MagicMock()
    entry_point.name = "acme"
    entry_point.load.return_value.return_value = stub()

    # Call test function
    with patch(f"{MODULE}.entry_points", return_value=[entry_point]) as entry_points:
        plugin = load_plugin("acme")

    # Assert the plugin was looked up in the right group and instantiated
    entry_points.assert_called_with(group=ENTRY_POINT_GROUP)
    assert plugin == entry_point.load.return_value.return_value


async def test_load_plugin_import_path():

    # Call test function
    plugin = load_plugin("centreon_mcp.auth.none:NoAuthPlugin")

    # Assert result
    assert isinstance(plugin, NoAuthPlugin)


async def test_load_plugin_unknown():

    # Call test function
    with (
        patch(f"{MODULE}.entry_points", return_value=[]),
        pytest.raises(ValueError, match="Unknown authentication plugin 'missing'"),
    ):
        _ = load_plugin("missing")


async def test_require_role_without_authentication():

    # Mock an unauthenticated server
    plugin = MagicMock()
    plugin.auth_provider.return_value = None

    # Setup args
    context = MagicMock()
    context.token = None

    # Call test function: every tool is granted, Centreon rights already apply
    with patch(f"{MODULE}.plugin", plugin):
        assert await require_role(Role.ADMIN)(context) is True


async def test_require_role_without_token():

    # Mock an authenticated server reached without a token
    plugin = MagicMock()
    context = MagicMock()
    context.token = None

    # Call test function
    with patch(f"{MODULE}.plugin", plugin):
        assert await require_role(Role.READER)(context) is False


@pytest.mark.parametrize(
    "role,level,granted",
    [
        (Role.READER, Role.READER, True),
        (Role.READER, Role.EDITOR, False),
        (Role.READER, Role.ADMIN, False),
        (Role.EDITOR, Role.READER, True),
        (Role.EDITOR, Role.EDITOR, True),
        (Role.EDITOR, Role.ADMIN, False),
        (Role.ADMIN, Role.READER, True),
        (Role.ADMIN, Role.EDITOR, True),
        (Role.ADMIN, Role.ADMIN, True),
    ],
)
async def test_require_role(role: Role, level: Role, granted: bool):

    # Mock an authenticated user holding the given role
    plugin = MagicMock()
    plugin.role = AsyncMock(return_value=role)

    # Setup args
    context = MagicMock()

    # Call test function
    with patch(f"{MODULE}.plugin", plugin):
        assert await require_role(level)(context) is granted

    # Assert the role was resolved from the request token
    plugin.role.assert_awaited_once_with(context.token)


@pytest.mark.parametrize(
    "plugin,missing",
    [
        # A plugin that implements nothing at all
        (object(), "auth_provider"),
        # A plugin that forgot one method of the contract, the likeliest mistake
    ],
)
async def test_load_plugin_rejects_an_incomplete_plugin(plugin: object, missing: str):

    # Call test function: a plugin missing part of the contract must fail at load, not on the
    # first request of the first user
    with (
        patch(f"{MODULE}.import_plugin", return_value=plugin),
        pytest.raises(TypeError, match=missing),
    ):
        _ = load_plugin("none")


async def test_load_plugin_names_the_setting_when_the_import_fails():

    # Call test function: the operator gets the setting to fix, not a bare import traceback
    with pytest.raises(ValueError, match="CENTREON_AUTH_PLUGIN 'nowhere:Missing'"):
        _ = load_plugin("nowhere:Missing")
