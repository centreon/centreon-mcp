from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import HTTPStatusError, Request, Response

from centreon_mcp import settings
from centreon_mcp.auth.base import Tenant
from centreon_mcp.utils.request import CentreonAPIError, hide, redact, request

MODULE = "centreon_mcp.utils.request"


@pytest.mark.parametrize(
    "headers,result",
    [
        (None, None),
        (
            {"X-AUTH-TOKEN": "centreon-api-token"},
            {"X-AUTH-TOKEN": "************-token"},
        ),
        # A token short enough for the tail to give it away is hidden whole
        ({"X-AUTH-TOKEN": "abcdef"}, {"X-AUTH-TOKEN": "[redacted]"}),
        ({"X-AUTH-TOKEN": "abcdefghijkl"}, {"X-AUTH-TOKEN": "[redacted]"}),
        # Headers carrying no token are left alone rather than raising inside the logger
        ({"Accept": "application/json"}, {"Accept": "application/json"}),
    ],
)
async def test_hide(headers: dict | None, result: dict | None):

    # Call test function
    assert hide(headers) == result


@pytest.mark.parametrize(
    "token",
    ["header-token", None],
)
@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_request(logger: MagicMock, plugin: MagicMock, token: str | None):

    # Setup args
    method = "GET"
    endpoint = "some/endpoint"
    params: dict = {}
    payload: dict = {}

    # Mock logger
    logger.debug.return_value = None

    # Mock the tenant resolved by the authentication plugin
    plugin.tenant = AsyncMock(
        return_value=Tenant(name="centreon", base_url=str(settings.base_url), api_token=token)
    )

    # Mock the shared client's response (client is the global mocked in conftest.py)
    content: dict = {}
    client, response = MagicMock(), MagicMock()
    response.json.return_value = content
    client.request = AsyncMock(return_value=response)

    # Call test function
    with patch(f"{MODULE}.client", client):
        result = await request(method, endpoint, payload, params)

    # Assert logger was called
    assert logger.debug.call_count == 2

    # Assert request was called with good args
    url = f"{settings.base_url}/api/latest/{endpoint}"
    headers = {"X-AUTH-TOKEN": token} if token else None
    client.request.assert_awaited_once_with(
        method, url, headers=headers, json=payload, params=params
    )

    # Assert request output
    assert result == content


@patch("centreon_mcp.auth.plugin", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_request_centreon_api_error(logger: MagicMock, plugin: MagicMock):

    # Setup args
    method = "GET"
    endpoint = "some/endpoint"
    params: dict = {}
    payload: dict = {}

    # Mock logger
    logger.debug.return_value = None

    # Mock the tenant resolved by the authentication plugin
    plugin.tenant = AsyncMock(
        return_value=Tenant(name="centreon", base_url=str(settings.base_url), api_token="token")
    )

    # Mock the shared client's response (client is the global mocked in conftest.py)
    content: dict = {}
    client, response = MagicMock(), MagicMock()
    response.json.return_value = content
    client.request = AsyncMock(return_value=response)

    # Mock response.raise_for_status to raise an error
    response.raise_for_status.side_effect = HTTPStatusError(
        message="Error",
        request=Request("GET", "http://localhost/api/latest/some/endpoint"),
        response=Response(500),
    )

    # Call test function
    with pytest.raises(CentreonAPIError), patch(f"{MODULE}.client", client):
        _ = await request(method, endpoint, payload, params)


async def test_request_client_not_initialized():

    # Simulate a client that was never initialized by the lifespan
    with (
        patch(f"{MODULE}.client", None),
        pytest.raises(RuntimeError, match="Centreon client is not initialized"),
    ):
        _ = await request("GET", "some/endpoint")


@pytest.mark.parametrize(
    "data,expected",
    [
        # Credentials travel in payloads
        (
            {"security": {"credentials": {"login": "svc", "password": "s3cr3t"}}},
            {"security": {"credentials": {"login": "svc", "password": "[redacted]"}}},
        ),
        # Tokens come back in responses, including freshly minted ones
        ({"security": {"token": "abc"}}, {"security": {"token": "[redacted]"}}),
        # Nested lists are walked too
        (
            {"items": [{"api_token": "a", "name": "keep"}]},
            {"items": [{"api_token": "[redacted]", "name": "keep"}]},
        ),
        # A macro says itself that it holds a password, under a key that names nothing
        (
            {"macros": [{"name": "MYSQLPASSWORD", "value": "s3cr3t", "is_password": True}]},
            {"macros": [{"name": "MYSQLPASSWORD", "value": "[redacted]", "is_password": True}]},
        ),
        # A macro that holds no password keeps its value, which is what makes a trace useful
        (
            {"macros": [{"name": "PORT", "value": "3306", "is_password": False}]},
            {"macros": [{"name": "PORT", "value": "3306", "is_password": False}]},
        ),
        # An SNMP community is a shared secret, whatever its neutral name suggests
        ({"snmp_community": "public"}, {"snmp_community": "[redacted]"}),
        # Everything else is left alone
        ({"id": 1, "name": "Central"}, {"id": 1, "name": "Central"}),
    ],
)
async def test_redact(data: dict, expected: dict):

    # Call test function
    assert redact(data) == expected


async def test_redact_leaves_the_original_alone():

    # Setup args
    data = {"password": "s3cr3t"}

    # Call test function
    _ = redact(data)

    # Assert the payload actually sent is untouched
    assert data == {"password": "s3cr3t"}
