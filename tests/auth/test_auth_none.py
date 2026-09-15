from unittest.mock import MagicMock, patch

import pytest

from centreon_mcp import settings
from centreon_mcp.auth.base import AuthenticationError, Role
from centreon_mcp.auth.none import LegacyPlugin

MODULE = "centreon_mcp.auth.none"


async def test_auth_provider():

    # Call test function: the MCP server itself stays unauthenticated
    assert LegacyPlugin().auth_provider() is None


@pytest.mark.parametrize(
    "headers,token",
    [
        ({"centreon-api-token": "header-token"}, "header-token"),
        ({}, "env-token"),
    ],
)
@patch(f"{MODULE}.get_http_headers", new_callable=MagicMock)
async def test_tenant(get_http_headers: MagicMock, headers: dict, token: str):

    # Mock the headers sent by the MCP client
    get_http_headers.return_value = headers

    # Call test function
    tenant = await LegacyPlugin().tenant(None)

    # Assert the Centreon and its token
    assert tenant.base_url == settings.base_url
    assert tenant.token == token


@patch(f"{MODULE}.get_http_headers", new_callable=MagicMock)
async def test_tenant_without_token(get_http_headers: MagicMock):

    # Mock a client sending no token
    get_http_headers.return_value = {}

    # Call test function
    with patch.object(settings, "api_token", None):
        tenant = await LegacyPlugin().tenant(None)

    # Assert no token is sent to Centreon
    assert tenant.token is None


@patch(f"{MODULE}.get_http_headers", new_callable=MagicMock)
async def test_tenant_without_base_url(get_http_headers: MagicMock):

    # Mock an incomplete configuration
    get_http_headers.return_value = {}

    # Call test function
    with (
        patch.object(settings, "base_url", None),
        pytest.raises(AuthenticationError, match="CENTREON_BASE_URL is required"),
    ):
        _ = await LegacyPlugin().tenant(None)


async def test_role():

    # Call test function: rights are carried by the Centreon token itself
    assert await LegacyPlugin().role(None) == Role.ADMIN


@patch(f"{MODULE}.get_http_headers", new_callable=MagicMock)
async def test_tenants(get_http_headers: MagicMock):

    # Mock the absence of a request context at startup
    get_http_headers.return_value = {}

    # Call test function
    tenants = LegacyPlugin().tenants()

    # Assert the single configured Centreon is returned
    assert [tenant.base_url for tenant in tenants] == [settings.base_url]


@patch(f"{MODULE}.get_http_headers", new_callable=MagicMock)
async def test_tenants_without_base_url(get_http_headers: MagicMock):

    # Mock the absence of a request context at startup
    get_http_headers.return_value = {}

    # Call test function: the misconfiguration stops the server rather than starting it blind
    with (
        patch.object(settings, "base_url", None),
        pytest.raises(AuthenticationError, match="CENTREON_BASE_URL is required"),
    ):
        _ = LegacyPlugin().tenants()
