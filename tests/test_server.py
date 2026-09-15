import importlib
from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest
from fastmcp.server.auth.auth import AuthProvider

from centreon_mcp import settings
from centreon_mcp.auth import Tenant
from centreon_mcp.server import check_tenants, health, icons, lifespan, mcp
from centreon_mcp.types.platform import Version
from centreon_mcp.utils.request import CentreonAPIError

MODULE = "centreon_mcp.server"

VERSION = Version(version="25.10.0", major="25", minor="10", fix="0")


def tenant(name: str) -> Tenant:
    """
    Build a tenant pointing at a fake Centreon.
    """
    return Tenant(name=name, base_url=f"http://{name}.example.com", api_token="token")


def unreachable() -> CentreonAPIError:
    """
    Build the error a Centreon that cannot be reached raises.
    """
    return CentreonAPIError(503, "http://example.com", "GET", {"message": "unreachable"})


@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.AsyncClient", new_callable=MagicMock)
@patch(f"{MODULE}.check_tenants", new_callable=AsyncMock)
async def test_lifespan(check_tenants: AsyncMock, async_client_cls: MagicMock, plugin: MagicMock):

    # Setup args
    app = MagicMock()

    # Mock a plugin adding no tool of its own
    plugin.components.return_value = []

    # Mock the Centreon client instantiated by the lifespan
    client = MagicMock()
    client.aclose = AsyncMock(return_value=None)
    async_client_cls.return_value = client

    # Mock import_server
    servers = [MagicMock(), MagicMock(), MagicMock()]
    app.mount = MagicMock()

    # Call test function, from a server that has not mounted anything yet
    with patch(f"{MODULE}.components", servers), patch(f"{MODULE}.mounted", False):
        async with lifespan(app):
            pass

    # Assert client instanciated with correct args
    async_client_cls.assert_called_once_with(timeout=settings.client_timeout)

    # Assert Centreon connectivity was checked
    check_tenants.assert_awaited_once_with()

    # Assert import_server called multiple times
    app.mount.assert_has_calls([call(s) for s in servers])

    # Assert client.aclose awaited once
    client.aclose.assert_awaited_once_with()


@patch(f"{MODULE}.Platform.get_web_version", new_callable=AsyncMock)
@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_check_tenants(logger: MagicMock, plugin: MagicMock, get_web_version: AsyncMock):

    # Setup args
    tenants = [tenant("first"), tenant("second")]
    plugin.tenants.return_value = tenants

    # Mock request
    get_web_version.return_value = VERSION

    # Call test function
    await check_tenants()

    # Assert every tenant was reached
    get_web_version.assert_has_awaits([call(tenant=t) for t in tenants])


@patch(f"{MODULE}.Platform.get_web_version", new_callable=AsyncMock)
@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_check_tenants_without_tenant(
    logger: MagicMock, plugin: MagicMock, get_web_version: AsyncMock
):

    # Setup args: a plugin that expects tenants and was given none, which is a misconfiguration
    plugin.tenants.return_value = []

    # Call test function
    await check_tenants()

    # Assert the check was skipped, and reported as the fault it is rather than as the legitimate
    # dynamic case, which the sibling test covers
    get_web_version.assert_not_awaited()
    logger.error.assert_called_once()


@patch(f"{MODULE}.Platform.get_web_version", new_callable=AsyncMock)
@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_check_tenants_single_unreachable(
    logger: MagicMock, plugin: MagicMock, get_web_version: AsyncMock
):

    # Setup args
    plugin.tenants.return_value = [tenant("only")]

    # Mock an unreachable Centreon
    get_web_version.side_effect = unreachable()

    # Call test function: a single unreachable Centreon prevents the server from starting
    with pytest.raises(CentreonAPIError):
        await check_tenants()


@patch(f"{MODULE}.Platform.get_web_version", new_callable=AsyncMock)
@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_check_tenants_partially_unreachable(
    logger: MagicMock, plugin: MagicMock, get_web_version: AsyncMock
):

    # Setup args
    plugin.tenants.return_value = [tenant("down"), tenant("up")]

    # Mock the first Centreon being unreachable
    get_web_version.side_effect = [unreachable(), VERSION]

    # Call test function: one unreachable tenant does not take the shared server down
    await check_tenants()

    # Assert the failure was reported, and the degraded startup named the tenant
    logger.warning.assert_called_once()
    assert "down" in logger.error.call_args.args[0]


@patch(f"{MODULE}.Platform.get_web_version", new_callable=AsyncMock)
@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_check_tenants_all_unreachable(
    logger: MagicMock, plugin: MagicMock, get_web_version: AsyncMock
):

    # Setup args
    plugin.tenants.return_value = [tenant("first"), tenant("second")]

    # Mock every Centreon being unreachable
    get_web_version.side_effect = unreachable()

    # Call test function
    with pytest.raises(RuntimeError, match="unreachable for every tenant: first, second"):
        await check_tenants()


@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.AsyncClient", new_callable=MagicMock)
@patch(f"{MODULE}.check_tenants", new_callable=AsyncMock)
async def test_lifespan_mounts_plugin_components(
    check_tenants: AsyncMock, async_client_cls: MagicMock, plugin: MagicMock
):

    # Setup args
    app = MagicMock()
    app.mount = MagicMock()

    # Mock the Centreon client instantiated by the lifespan
    client = MagicMock()
    client.aclose = AsyncMock(return_value=None)
    async_client_cls.return_value = client

    # Mock a plugin contributing its own tools
    contributed = MagicMock()
    plugin.components.return_value = [contributed]

    # Call test function
    built_in = [MagicMock()]
    with patch(f"{MODULE}.components", built_in), patch(f"{MODULE}.mounted", False):
        async with lifespan(app):
            pass

    # Assert the plugin tools were mounted alongside the built-in ones
    app.mount.assert_has_calls([call(built_in[0]), call(contributed)])


@pytest.mark.parametrize("icon", ["https://example.com/logo.png", None])
async def test_icons(icon: str | None):

    # Call test function: a deployment that sets no icon is identified by its name alone
    with patch.object(settings, "mcp_icon_url", icon):
        result = icons()

    assert (result[0].src if result else None) == icon


async def test_server_identity():

    # Call test function: the consent screen names this server
    assert mcp.name == "Centreon MCP Server"


async def test_health():

    # Call test function: the probe of an orchestrator must not depend on Centreon
    response = await health(MagicMock())

    assert response.status_code == 200
    assert response.body == b'{"status":"ok"}'


@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
async def test_server_is_built_with_the_plugin_provider(plugin: MagicMock):

    # Mock a plugin authenticating its users
    provider = MagicMock(spec=AuthProvider)
    plugin.auth_provider.return_value = provider

    # Call test function: rebuilding the module is what wires the provider into the server
    module = importlib.reload(importlib.import_module(MODULE))

    # Assert the server delegates authentication to the plugin rather than staying open
    assert module.mcp.auth is provider

    # Restore the module the rest of the suite imported
    importlib.reload(module)


@patch(f"{MODULE}.Platform.get_web_version", new_callable=AsyncMock)
@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_check_tenants_resolved_per_request(
    logger: MagicMock, plugin: MagicMock, get_web_version: AsyncMock
):

    # Setup args: a plugin resolving its Centreon from the identity of each request knows none
    plugin.tenants.return_value = None

    # Call test function
    await check_tenants()

    # Assert the check was skipped without crying misconfiguration, unlike an empty sequence
    get_web_version.assert_not_awaited()
    logger.info.assert_called_once()
    logger.warning.assert_not_called()


@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.AsyncClient", new_callable=MagicMock)
@patch(f"{MODULE}.check_tenants", new_callable=AsyncMock)
async def test_lifespan_mounts_once(
    check_tenants: AsyncMock, async_client_cls: MagicMock, plugin: MagicMock
):

    # Setup args
    app = MagicMock()
    app.mount = MagicMock()
    plugin.components.return_value = []
    client = MagicMock()
    client.aclose = AsyncMock(return_value=None)
    async_client_cls.return_value = client

    # Call test function twice, as an app started again in the same process would
    with patch(f"{MODULE}.components", [MagicMock()]), patch(f"{MODULE}.mounted", False):
        async with lifespan(app):
            pass
        async with lifespan(app):
            pass

    # Assert the tools were mounted once: duplicates shadow each other in listings
    app.mount.assert_called_once()
