from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.auth import AuthenticationError, Role, Tenant
from centreon_mcp.components.account import get_current_context

MODULE = "centreon_mcp.components.account"


@patch(f"{MODULE}.get_access_token", new_callable=MagicMock)
@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_get_current_context(
    logger: MagicMock, plugin: MagicMock, get_access_token: MagicMock
):

    # Mock an authenticated user
    token = MagicMock()
    get_access_token.return_value = token
    plugin.tenant = AsyncMock(
        return_value=Tenant(name="customer", base_url="http://customer.example.com")
    )
    plugin.role = AsyncMock(return_value=Role.EDITOR)

    # Call test function
    result = await get_current_context()

    # Assert the tenant and the role were resolved from the request token
    plugin.tenant.assert_awaited_once_with(token)
    plugin.role.assert_awaited_once_with(token)

    # Assert result
    assert result.tenant == "customer"
    assert result.role == "editor"
    assert result.authenticated is True


@patch(f"{MODULE}.get_access_token", new_callable=MagicMock)
@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_get_current_context_unauthenticated(
    logger: MagicMock, plugin: MagicMock, get_access_token: MagicMock
):

    # Mock an unauthenticated server
    get_access_token.return_value = None
    plugin.tenant = AsyncMock(
        return_value=Tenant(name="centreon", base_url="http://centreon.example.com")
    )
    plugin.role = AsyncMock(return_value=Role.ADMIN)

    # Call test function
    result = await get_current_context()

    # Assert result
    assert result.role == "admin"
    assert result.authenticated is False


@patch(f"{MODULE}.get_access_token", new_callable=MagicMock)
@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_get_current_context_explains_a_refusal(
    logger: MagicMock, plugin: MagicMock, get_access_token: MagicMock
):

    # Mock a user whose organization reaches no Centreon and holds no level
    get_access_token.return_value = MagicMock()
    plugin.tenant = AsyncMock(side_effect=AuthenticationError("Organization acme is not served"))
    plugin.role = AsyncMock(side_effect=AuthenticationError("No role held in acme"))

    # Call test function: this is the one tool such a user reaches, so it answers rather than fails
    result = await get_current_context()

    # Assert the reasons reached the user, since nothing else will tell them
    assert result.tenant is None
    assert result.role == "none"
    assert result.detail == "Organization acme is not served. No role held in acme"
