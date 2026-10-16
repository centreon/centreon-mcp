from unittest.mock import AsyncMock, MagicMock, call, patch

from centreon_mcp import settings
from centreon_mcp.__main__ import health, lifespan, main
from centreon_mcp.components import components
from centreon_mcp.types.platform import Version

MODULE = "centreon_mcp.__main__"


@patch(f"{MODULE}.mcp", new_callable=MagicMock)
@patch(f"{MODULE}.auth", new_callable=MagicMock)
def test_main(auth: MagicMock, mcp: MagicMock):

    # Mock mcp.run
    mcp.run.return_value = None

    # Call test function
    main()

    # Assert auth.load called once
    auth.load.assert_called_once_with()

    # Assert all components are mounted
    mcp.mount.assert_has_calls([call(component) for component in components])

    # Assert mcp.run called with rigt args
    mcp.run.assert_called_once_with(
        transport="http", host=settings.mcp_host, port=settings.mcp_port
    )


@patch(f"{MODULE}.AsyncClient", new_callable=MagicMock)
@patch(f"{MODULE}.Platform.get_web_version", new_callable=AsyncMock)
@patch(f"{MODULE}.auth", new_callable=MagicMock)
async def test_lifespan(
    auth: MagicMock, platform_get_web_version: AsyncMock, async_client_cls: MagicMock
):

    # Setup args
    app = MagicMock()

    # Mock the Centreon client instantiated by the lifespan
    client = MagicMock()
    client.aclose = AsyncMock(return_value=None)
    async_client_cls.return_value = client

    # Mock auth plugin to return fake tenants
    tenants = [MagicMock(), MagicMock(), MagicMock()]
    auth.plugin.tenants = AsyncMock(return_value=tenants)

    # Mock Platform.get_web_version
    platform_get_web_version.side_effect = [
        Version(version="25.10.0", major="25", minor="10", fix=fix) for fix in ["0", "3", "5"]
    ]

    # Call test function
    async with lifespan(app):
        pass

    # Assert client instanciated with correct args
    async_client_cls.assert_called_once_with(
        verify=settings.verify, timeout=settings.client_timeout
    )

    # Assert Platform.get_web_version called with correct args
    platform_get_web_version.assert_has_awaits([call(tenant) for tenant in tenants])

    # Assert client.aclose awaited once
    client.aclose.assert_awaited_once_with()


async def test_health():

    # Setup args
    request = MagicMock()

    # Call test function
    response = await health(request)

    # Check response
    assert response.status_code == 200
