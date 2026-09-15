from unittest.mock import AsyncMock, patch

from centreon_mcp.auth import Tenant
from centreon_mcp.types.platform import Platform, Version

MODULE = "centreon_mcp.types.platform"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_platform_get_web_version(request: AsyncMock):

    # Mock request
    version = Version(version="25.10.00", major="25", minor="10", fix="00")
    request.return_value = {"web": version.model_dump()}

    # Call test function
    result = await Platform.get_web_version()

    # Assert request called with right args
    request.assert_awaited_once_with("GET", "platform/versions", tenant=None)

    # Assert result
    assert result == version


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_platform_get_web_version_for_tenant(request: AsyncMock):

    # Setup args
    tenant = Tenant(name="customer", base_url="http://customer.example.com", api_token="token")

    # Mock request
    version = Version(version="25.10.00", major="25", minor="10", fix="00")
    request.return_value = {"web": version.model_dump()}

    # Call test function
    result = await Platform.get_web_version(tenant=tenant)

    # Assert request targeted the given tenant
    request.assert_awaited_once_with("GET", "platform/versions", tenant=tenant)

    # Assert result
    assert result == version
