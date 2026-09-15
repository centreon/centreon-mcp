from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastmcp import Client

from centreon_mcp.auth import ADMIN, AUTHENTICATED, EDITOR, READER, AuthenticationError, Role
from centreon_mcp.components import components
from centreon_mcp.server import mcp
from centreon_mcp.types.platform import Version

# The permission level every tool requires, mirroring the table published in TOOLS.md
LEVELS = {
    "list_configurations": READER,
    "create_configuration": EDITOR,
    "update_configuration": EDITOR,
    "delete_configurations": ADMIN,
    "manage_monitoring_server_configurations": ADMIN,
    "list_monitoring_resources": READER,
    "list_monitoring_entities": READER,
    "list_monitoring_actions": READER,
    "set_monitoring_actions": EDITOR,
    "cancel_monitoring_actions": EDITOR,
    "count_monitoring_resources_by_status": READER,
    "get_host_timeline": READER,
    "get_service_timeline": READER,
    "get_service_metrics": READER,
    "get_current_context": AUTHENTICATED,
}


def up_to(*levels) -> list[str]:
    """
    Return the tools a user holding the highest of the given levels sees.
    """
    return sorted(name for name, level in LEVELS.items() if level in levels)


NO_LEVEL = up_to(AUTHENTICATED)
READ_ONLY = up_to(AUTHENTICATED, READER)
UP_TO_EDITOR = up_to(AUTHENTICATED, READER, EDITOR)
EVERY_TOOL = sorted(LEVELS)

VERSION = Version(version="25.10.0", major="25", minor="10", fix="0")


def build_plugin(role: Role | None = None, error: Exception | None = None) -> MagicMock:
    """
    Mock a plugin resolving the given role, or failing to resolve any.
    """
    plugin = MagicMock()
    # No tenant is known upfront, so the startup check has nothing to reach
    plugin.tenants.return_value = []
    if role is None and error is None:
        plugin.auth_provider.return_value = None
    else:
        plugin.role = AsyncMock(return_value=role, side_effect=error)
    return plugin


def serve(plugin: MagicMock):
    """
    Patch the server so that a client talks to it as the user the plugin describes.
    """
    return (
        patch(
            "centreon_mcp.server.Platform.get_web_version",
            new_callable=AsyncMock,
            return_value=VERSION,
        ),
        patch("centreon_mcp.auth.plugin", plugin),
        patch("fastmcp.server.dependencies.get_access_token", return_value=MagicMock()),
    )


async def list_tools(role: Role | None = None) -> list[str]:
    """
    List the tools an MCP client sees, optionally as a user holding the given role.

    Passing no role exercises an unauthenticated server, where the authorization checks are
    expected to grant every tool.
    """
    version, plugin, token = serve(build_plugin(role))
    with version, plugin, token:
        async with Client(mcp) as client:
            return sorted(tool.name for tool in await client.list_tools())


async def test_tools_declare_a_role():

    # Call test function: gather the tools as registered on each component
    registered = {
        tool.name: tool for component in components for tool in await component._list_tools()
    }

    # Assert every tool is gated, so a new one cannot ship ungated by accident
    assert sorted(registered) == EVERY_TOOL
    for name, tool in registered.items():
        assert tool.auth is LEVELS[name], f"{name} does not require the expected role"


async def test_list_tools_unauthenticated():

    # Call test function: without an identity provider the server exposes every tool
    assert await list_tools() == EVERY_TOOL


@pytest.mark.parametrize(
    "role,expected",
    [
        (Role.NONE, NO_LEVEL),
        (Role.READER, READ_ONLY),
        (Role.EDITOR, UP_TO_EDITOR),
        (Role.ADMIN, EVERY_TOOL),
    ],
)
async def test_list_tools_by_role(role: Role, expected: list[str]):

    # Call test function: tools above the user level are hidden from the listing
    assert await list_tools(role) == expected


@patch("centreon_mcp.auth.logger", new_callable=MagicMock)
async def test_list_tools_when_the_plugin_fails(logger: MagicMock):

    # Mock a plugin that cannot resolve a role, a network failure for instance
    plugin = build_plugin(error=RuntimeError("identity provider is down"))

    # Call test function: a plugin that cannot answer denies rather than grants
    version, patched, token = serve(plugin)
    with version, patched, token:
        async with Client(mcp) as client:
            assert sorted(t.name for t in await client.list_tools()) == NO_LEVEL

    # Assert the cause was recorded, since the client only ever sees a missing tool
    assert "identity provider is down" in logger.error.call_args.args[0]


@patch("centreon_mcp.utils.mixins.request", new_callable=AsyncMock)
async def test_call_tool_denied(request: AsyncMock):

    # Mock a reader trying to reach a tool reserved to administrators
    plugin = build_plugin(Role.READER)

    # Call test function
    version, patched, token = serve(plugin)
    with version, patched, token:
        async with Client(mcp) as client:
            with pytest.raises(Exception, match="Unknown tool: 'delete_configurations'"):
                _ = await client.call_tool(
                    "delete_configurations", {"model_type": "host", "model_ids": [1]}
                )

    # Assert the tool body never ran, which is what denial has to mean
    request.assert_not_awaited()


async def test_list_tools_unauthenticated_on_an_authenticated_server():

    # Mock a server whose plugin authenticates its users, reached without a token
    plugin = build_plugin(Role.ADMIN)
    plugin.auth_provider.return_value = MagicMock()

    # Call test function: the bypass granting every tool applies only to an open server
    version, patched = serve(plugin)[:2]
    with version, patched:
        async with Client(mcp) as client:
            assert await client.list_tools() == []


@patch("centreon_mcp.auth.logger", new_callable=MagicMock)
async def test_list_tools_when_the_plugin_refuses(logger: MagicMock):

    # Mock a plugin refusing this identity on purpose, an unknown tenant for instance
    plugin = build_plugin(error=AuthenticationError("Organization acme is not served here"))

    # Call test function
    version, patched, token = serve(plugin)
    with version, patched, token:
        async with Client(mcp) as client:
            assert sorted(t.name for t in await client.list_tools()) == NO_LEVEL

    # Assert a deliberate refusal is reported as such, not as a fault with a traceback
    assert "not served here" in logger.info.call_args.args[0]
    logger.error.assert_not_called()


@pytest.mark.parametrize(
    "plugin",
    [
        build_plugin(error=AuthenticationError("Organization acme is not served here")),
        build_plugin(error=RuntimeError("identity provider is down")),
    ],
)
async def test_context_tool_stays_listed_when_the_plugin_grants_nothing(plugin: MagicMock):

    # Call test function: a tool requiring no level never asks the plugin for one, so it stays
    # listed for the users it exists to inform. That it also answers when called is pinned by
    # tests/components/test_component_account.py
    version, patched, token = serve(plugin)
    with version, patched, token:
        async with Client(mcp) as client:
            assert sorted(t.name for t in await client.list_tools()) == NO_LEVEL
