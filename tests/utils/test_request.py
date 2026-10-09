from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import HTTPStatusError, Request, Response

from centreon_mcp import settings
from centreon_mcp.utils.request import REDACTED, CentreonAPIError, hide, redact, request

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
@patch(f"{MODULE}.get_http_headers", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_request(logger: MagicMock, get_http_headers: MagicMock, token: str | None):

    # Setup args
    method = "GET"
    endpoint = "some/endpoint"
    params: dict = {}
    payload: dict = {}

    # Mock logger
    logger.debug.return_value = None

    # Mock get_http_hearders
    get_http_headers.return_value = {"centreon-api-token": token} if token else {}

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
    headers = {"X-AUTH-TOKEN": token or settings.api_token}
    client.request.assert_awaited_once_with(
        method, endpoint, headers=headers, json=payload, params=params
    )

    # Assert request output
    assert result == content


@patch(f"{MODULE}.get_http_headers", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_request_centreon_api_error(logger: MagicMock, get_http_headers: MagicMock):

    # Setup args
    method = "GET"
    endpoint = "some/endpoint"
    params: dict = {}
    payload: dict = {}

    # Mock logger
    logger.debug.return_value = None

    # Mock get_http_hearders
    token = "token"
    get_http_headers.return_value = {"centreon-api-token": token}

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


@patch(f"{MODULE}.get_http_headers", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_request_redacts_the_exchange_it_logs(logger: MagicMock, get_http_headers: MagicMock):

    # Setup args: a payload carrying a credential, as a service creation does
    payload = {"macros": [{"name": "DBPASSWORD", "value": "s3cr3t", "is_password": True}]}
    get_http_headers.return_value = {"centreon-api-token": "long-enough-token"}

    # Mock a response carrying a token back, as a token creation does
    content = {"result": [{"token": "minted-token"}]}
    client, response = MagicMock(), MagicMock()
    response.json.return_value = content
    client.request = AsyncMock(return_value=response)

    # Call test function
    with patch(f"{MODULE}.client", client):
        _ = await request("POST", "some/endpoint", payload)

    # Assert neither secret reached the log, in either direction
    logged = " ".join(str(call) for call in logger.debug.call_args_list)
    assert "s3cr3t" not in logged
    assert "minted-token" not in logged
    assert logged.count(REDACTED) == 2

    # Assert the payload actually sent is untouched
    assert payload["macros"][0]["value"] == "s3cr3t"


@patch(f"{MODULE}.get_http_headers", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_request_redacts_the_error_it_raises(logger: MagicMock, get_http_headers: MagicMock):

    # Setup args
    get_http_headers.return_value = {"centreon-api-token": "token"}

    # Mock an error body that echoes back what was sent, which Centreon does
    content = {"message": "rejected", "password": "s3cr3t"}
    client, response = MagicMock(), MagicMock()
    response.json.return_value = content
    response.raise_for_status.side_effect = HTTPStatusError(
        message="Error",
        request=Request("POST", "http://centreon.example.com/api/latest/some/endpoint"),
        response=Response(400),
    )
    client.request = AsyncMock(return_value=response)

    # Call test function
    with patch(f"{MODULE}.client", client), pytest.raises(CentreonAPIError) as raised:
        _ = await request("POST", "some/endpoint")

    # Assert the error reaching the MCP client carries no credential: its content is rendered
    # back to the caller, so redacting only the logs would not be enough
    assert "s3cr3t" not in str(raised.value)
    assert raised.value.content["password"] == REDACTED


@pytest.mark.parametrize(
    "field",
    [
        "access_token",
        "api_key",
        "api_token",
        "authorization",
        "authtoken",
        "client_secret",
        "password",
        "private_key",
        "refresh_token",
        "secret",
        "snmp_community",
        "token",
    ],
)
async def test_redact_covers_every_declared_secret(field: str):

    # Call test function: the list is spelled out here rather than derived from SECRET_FIELDS,
    # so removing a name from the set fails this test instead of silently shrinking it
    assert redact({field: "s3cr3t"}) == {field: REDACTED}

    # Assert the match ignores case, as a Centreon payload spelling differs from ours
    assert redact({field.upper(): "s3cr3t"}) == {field.upper(): REDACTED}
