from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.auth import AuthenticationError, Role
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
    plugin.role = AsyncMock(return_value=Role.EDITOR)

    # Call test function
    result = await get_current_context()

    # Assert the level was resolved from the request token
    plugin.role.assert_awaited_once_with(token)

    # Assert result
    assert result.role == "editor"
    assert result.authenticated is True
    assert result.detail is None


@patch(f"{MODULE}.get_access_token", new_callable=MagicMock)
@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_get_current_context_unauthenticated(
    logger: MagicMock, plugin: MagicMock, get_access_token: MagicMock
):

    # Mock an unauthenticated server
    get_access_token.return_value = None
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

    # Mock a user the deployment grants nothing to
    get_access_token.return_value = MagicMock()
    plugin.role = AsyncMock(side_effect=AuthenticationError("No role held in acme"))

    # Call test function: this is the one tool such a user reaches, so it answers rather than fails
    result = await get_current_context()

    # Assert the reason reached the user, since nothing else will tell them
    assert result.role == "none"
    assert result.detail == "No role held in acme"


@patch(f"{MODULE}.get_access_token", new_callable=MagicMock)
@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_get_current_context_survives_a_broken_plugin(
    logger: MagicMock, plugin: MagicMock, get_access_token: MagicMock
):

    # Mock a plugin that cannot answer at all, a provider outage for instance
    get_access_token.return_value = MagicMock()
    plugin.role = AsyncMock(side_effect=RuntimeError("identity provider is down"))

    # Call test function: the tool a user falls back on must answer, not fail with them
    result = await get_current_context()

    # Assert the user is told something actionable without being shown the internal failure
    assert result.role == "none"
    assert "could not determine" in result.detail

    # Assert the cause was recorded server side, since the answer deliberately omits it
    logger.error.assert_called_once()
