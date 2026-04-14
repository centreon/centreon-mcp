from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import HTTPStatusError, Request, Response

from centreon_mcp import CREDENTIALS
from centreon_mcp.utils.request import CentreonAPIError, request

MODULE = "centreon_mcp.utils.request"


@patch(f"{MODULE}.AsyncClient", new_callable=MagicMock)
@patch(f"{MODULE}.get_http_headers", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_request(
    logger: MagicMock, get_http_headers: MagicMock, client_cls: MagicMock
):

    # Setup args
    method = "GET"
    endpoint = "some/endpoint"
    params: dict = {}
    payload: dict = {}
    timeout = 10

    # Mock logger
    logger.debug.return_value = None

    # Mock get_http_hearders
    token = "token"
    get_http_headers.return_value = {"centreon-api-token": token}

    # Mock AsyncClient.request
    content: dict = {}
    client, response = AsyncMock(), MagicMock()
    response.json.return_value = content
    client.request.return_value = response
    context_manager = AsyncMock()
    context_manager.__aenter__.return_value = client
    context_manager.__aexit__.return_value = None
    client_cls.return_value = context_manager

    # Call test function
    result = await request(method, endpoint, payload, params, timeout)

    # Assert logger was called
    assert logger.debug.call_count == 2

    # Assert request was called with good args
    base = CREDENTIALS["CENTREON_BASE_URL"]
    url = f"{base}/api/latest/{endpoint}"
    headers = {"X-AUTH-TOKEN": token}
    client.request.assert_awaited_once_with(
        method, url, headers=headers, json=payload, params=params, timeout=timeout
    )

    # Assert request output
    assert result == content


@patch(f"{MODULE}.AsyncClient", new_callable=MagicMock)
@patch(f"{MODULE}.get_http_headers", new_callable=MagicMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_request_centreon_api_error(
    logger: MagicMock, get_http_headers: MagicMock, client_cls: MagicMock
):

    # Setup args
    method = "GET"
    endpoint = "some/endpoint"
    params: dict = {}
    payload: dict = {}
    timeout = 10

    # Mock logger
    logger.debug.return_value = None

    # Mock get_http_hearders
    token = "token"
    get_http_headers.return_value = {"centreon-api-token": token}

    # Mock AsyncClient.request
    content: dict = {}
    client, response = AsyncMock(), MagicMock()
    response.json.return_value = content
    client.request.return_value = response
    context_manager = AsyncMock()
    context_manager.__aenter__.return_value = client
    context_manager.__aexit__.return_value = None
    client_cls.return_value = context_manager

    # Mock response.raise_for_status to raise an error
    response.raise_for_status.side_effect = HTTPStatusError(
        message="Error",
        request=Request("GET", "http://localhost/api/latest/some/endpoint"),
        response=Response(500),
    )

    # Call test function
    with pytest.raises(CentreonAPIError):
        _ = await request(method, endpoint, payload, params, timeout)
