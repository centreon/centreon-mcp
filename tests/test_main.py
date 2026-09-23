import importlib
from unittest.mock import AsyncMock, MagicMock, call, patch

from fastmcp.server.auth.auth import AuthProvider

from centreon_mcp import settings
from centreon_mcp.__main__ import health, lifespan, main
from centreon_mcp.types.platform import Version

MODULE = "centreon_mcp.__main__"

VERSION = Version(version="25.10.0", major="25", minor="10", fix="0")


@patch(f"{MODULE}.mcp")
def test_main(mcp: MagicMock):

    # Mock mcp.run
    mcp.run.return_value = None

    # Call test function
    main()

    # Assert mcp.run called with rigt args
    mcp.run.assert_called_once_with(
        transport="http", host=settings.mcp_host, port=settings.mcp_port
    )


@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.AsyncClient", new_callable=MagicMock)
@patch(f"{MODULE}.Platform.get_web_version", new_callable=AsyncMock)
async def test_lifespan(get_web_version: AsyncMock, async_client_cls: MagicMock, plugin: MagicMock):

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
    async_client_cls.assert_called_once_with(
        verify=settings.verify, timeout=settings.client_timeout
    )

    # Assert Centreon connectivity was checked
    get_web_version.assert_awaited_once_with()

    # Assert import_server called multiple times
    app.mount.assert_has_calls([call(s) for s in servers])

    # Assert client.aclose awaited once
    client.aclose.assert_awaited_once_with()


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


@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.AsyncClient", new_callable=MagicMock)
@patch(f"{MODULE}.Platform.get_web_version", new_callable=AsyncMock)
async def test_lifespan_mounts_once(
    get_web_version: AsyncMock, async_client_cls: MagicMock, plugin: MagicMock
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
