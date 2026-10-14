from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import HTTPStatusError, Request, Response
from pydantic import SecretStr

from centreon_mcp.auth.models import Tenant
from centreon_mcp.utils.request import CentreonAPIError, hide, request

MODULE = "centreon_mcp.utils.request"


@pytest.mark.parametrize(
    "headers,result",
    [
        (None, None),
        (
            {"X-AUTH-TOKEN": "centreon-api-token"},
            {"X-AUTH-TOKEN": "************-token"},
        ),
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
@patch(f"{MODULE}.auth", new_callable=MagicMock)
async def test_request(
    auth: MagicMock, logger: MagicMock, get_http_headers: MagicMock, token: str | None
):

    # Setup args
    method = "GET"
    endpoint = "some/endpoint"
    params: dict = {}
    payload: dict = {}
    tenant = Tenant(
        name="default", base_url="http://centreon.example.com", api_token=SecretStr("tenant-token")
    )

    # Mock auth plugin
    auth.plugin.tenant = AsyncMock(return_value=tenant)

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
    url = f"{tenant.base_url}/api/latest/{endpoint}"
    headers = {"X-AUTH-TOKEN": token or tenant.token}
    client.request.assert_awaited_once_with(
        method, url, headers=headers, json=payload, params=params
    )

    # Assert request output
    assert result == content


@patch(f"{MODULE}.get_http_headers", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
@patch(f"{MODULE}.auth", new_callable=MagicMock)
async def test_request_centreon_api_error(
    auth: MagicMock, logger: MagicMock, get_http_headers: MagicMock
):

    # Setup args
    method = "GET"
    endpoint = "some/endpoint"
    params: dict = {}
    payload: dict = {}

    # Mock auth plugin
    auth.plugin.tenant = AsyncMock(
        return_value=Tenant(name="default", base_url="http://centreon.example.com")
    )

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


def test_centreon_api_error_str():

    # Build error
    error = CentreonAPIError(
        status=404,
        url="http://centreon.example.com/api/latest/some/endpoint",
        method="GET",
        content={"code": 404, "message": "Not found"},
    )

    # Assert string representation
    assert str(error) == (
        "\nCentreon API Error [404]"
        "\nMethod: GET"
        "\nURL: http://centreon.example.com/api/latest/some/endpoint"
        "\nContent:\n  code: 404\n  message: Not found"
    )


@patch(f"{MODULE}.get_http_headers", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
@patch(f"{MODULE}.auth", new_callable=MagicMock)
async def test_request_non_json_response(
    auth: MagicMock, logger: MagicMock, get_http_headers: MagicMock
):

    # Mock auth plugin
    auth.plugin.tenant = AsyncMock(
        return_value=Tenant(name="default", base_url="http://centreon.example.com")
    )

    # Mock get_http_hearders
    get_http_headers.return_value = {"centreon-api-token": "token"}

    # Mock the shared client's response with a non-JSON body
    client = MagicMock()
    response = Response(
        200,
        text="<html>Not JSON</html>",
        request=Request("GET", "http://centreon.example.com/api/latest/some/endpoint"),
    )
    client.request = AsyncMock(return_value=response)

    # Call test function
    with patch(f"{MODULE}.client", client):
        result = await request("GET", "some/endpoint")

    # Assert raw text is returned and a warning was logged
    assert result == {"raw": "<html>Not JSON</html>"}
    logger.warning.assert_called_once()
    assert "Non-JSON response from GET" in logger.warning.call_args.args[0]
