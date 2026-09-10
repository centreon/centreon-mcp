from unittest.mock import AsyncMock, MagicMock, call, patch

from centreon_mcp import settings
from centreon_mcp.server import lifespan
from centreon_mcp.types.platform import Version

MODULE = "centreon_mcp.server"


@patch(f"{MODULE}.AsyncClient", new_callable=MagicMock)
@patch(f"{MODULE}.Platform.get_web_version", new_callable=AsyncMock)
async def test_lifespan(platform_get_web_version: AsyncMock, async_client_cls: MagicMock):

    # Setup args
    app = MagicMock()

    # Mock the Centreon client instantiated by the lifespan
    client = MagicMock()
    client.aclose = AsyncMock(return_value=None)
    async_client_cls.return_value = client

    # Mock request
    version = Version(version="25.10.0", major="25", minor="10", fix="0")
    platform_get_web_version.return_value = version

    # Mock import_server
    servers = [MagicMock(), MagicMock(), MagicMock()]
    app.mount = MagicMock()

    # Call test function
    with patch(f"{MODULE}.components", servers):
        async with lifespan(app):
            pass

    # Assert client instanciated with correct args
    async_client_cls.assert_called_once_with(timeout=settings.client_timeout)

    # Assert request called with right args
    platform_get_web_version.assert_awaited_once()

    # Assert import_server called multiple times
    app.mount.assert_has_calls([call(s) for s in servers])

    # Assert client.aclose awaited once
    client.aclose.assert_awaited_once_with()
