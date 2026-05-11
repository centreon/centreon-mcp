from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

from centreon_mcp.server import lifespan
from centreon_mcp.types.platform import Version

MODULE = "centreon_mcp.server"


@patch(f"{MODULE}.Platform.get_web_version", new_callable=AsyncMock)
async def test_lifespan(platform_get_web_version: AsyncMock):

    # Setup args
    app = MagicMock()

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

    # Assert request called with right args
    platform_get_web_version.assert_awaited_once()

    # Assert import_server called multiple times
    app.mount.assert_has_calls([call(s) for s in servers])


@patch(f"{MODULE}.CREDENTIALS", {"CENTREON_BASE_URL": ""})
async def test_lifespan_missing_base_url_raises():

    # Setup args
    app = MagicMock()

    # Call test funtion
    with pytest.raises(RuntimeError, match="CENTREON_BASE_URL is missing"):
        async with lifespan(app):
            pass
