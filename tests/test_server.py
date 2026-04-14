from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from centreon_mcp.server import lifespan
from centreon_mcp.utils.request import CentreonAPIError

MODULE = "centreon_mcp.server"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_lifespan(request: AsyncMock):

    # Setup args
    app = MagicMock()

    # Mock request
    request.return_value = {"web": {"version": "24.10.0"}}

    # Mock import_server
    servers = [MagicMock(), MagicMock(), MagicMock()]
    app.import_server = AsyncMock()

    # Call test function
    with patch(f"{MODULE}.components", servers):
        async with lifespan(app):
            pass

    # Assert request called with right args
    request.assert_awaited_once_with("GET", "platform/versions")

    # Assert import_server called multiple times
    assert app.import_server.await_count == len(servers)


@patch(f"{MODULE}.CREDENTIALS", {"CENTREON_BASE_URL": ""})
async def test_lifespan_missing_base_url_raises():

    # Setup args
    app = MagicMock()

    # Call test funtion
    with pytest.raises(RuntimeError, match="CENTREON_BASE_URL is missing"):
        async with lifespan(app):
            pass


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_lifespan_centreon_api_error(request: AsyncMock):

    # Setup args
    app = MagicMock()

    # Mock request to raise CentreonAPIError
    request.side_effect = CentreonAPIError(status=401, url="https://fake.host/api/latest/", method="GET", content={"message": "Unauthorized"})

    with pytest.raises(CentreonAPIError):
        async with lifespan(app):
            pass
