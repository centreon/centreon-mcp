import json
from copy import deepcopy

from fastmcp.server.dependencies import get_http_headers
from httpx import AsyncClient, HTTPStatusError

from centreon_mcp import CREDENTIALS
from centreon_mcp.utils import logger

_client: AsyncClient | None = None


def get_client() -> AsyncClient:
    """
    Return the shared Centreon HTTP client, creating it on first use.
    """
    global _client
    if _client is None or _client.is_closed:
        _client = AsyncClient()
    return _client


async def close_client() -> None:
    """
    Close the shared Centreon HTTP client.
    """
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


def hide(headers: dict | None) -> dict | None:
    """
    Hide Centreon API token in headers for logging
    """
    if headers is None:
        return None

    hidden = deepcopy(headers)
    token = headers["X-AUTH-TOKEN"]
    size = 6
    hidden["X-AUTH-TOKEN"] = (len(token) - size) * "*" + token[-size:]
    return hidden


class CentreonAPIError(Exception):
    """
    Custom exception for Centreon API errors.
    """

    def __init__(self, status: int, url: str, method: str, content: dict) -> None:
        self.status = status
        self.url = url
        self.method = method
        self.content = content

    def __str__(self) -> str:
        """
        Return string representation of the error.
        """
        content = "\n".join(f"  {key}: {value}" for key, value in self.content.items())
        return (
            f"\nCentreon API Error [{self.status}]"
            f"\nMethod: {self.method}"
            f"\nURL: {self.url}"
            f"\nContent:\n{content}"
        )


async def request(
    method: str, endpoint: str, payload: dict | None = None, params: dict | None = None
) -> dict:
    """
    Make request to Centreon API.
    """
    # Build request arguments
    base = CREDENTIALS["CENTREON_BASE_URL"]
    token = get_http_headers().get("centreon-api-token") or CREDENTIALS["CENTREON_API_TOKEN"]
    url = f"{base}/api/latest/{endpoint}"
    headers = {"X-AUTH-TOKEN": token} if token else None
    params = params or {}
    params = {name: value for name, value in params.items() if value is not None}

    # Make request and handle response
    logger.debug(
        f"Centreon API Request: {method} {url}\n"
        f"Headers: {json.dumps(hide(headers), indent=2)}\n"
        f"Params: {json.dumps(params, indent=2)}\n"
        f"Payload: {json.dumps(payload, indent=2)}"
    )
    try:
        client = get_client()
        response = await client.request(method, url, headers=headers, json=payload, params=params)
        try:
            content = response.json() if (response.status_code != 204 and response.content) else {}
        except json.JSONDecodeError:
            logger.warning(
                f"Non-JSON response from {method} {url} (status {response.status_code}): {response.text[:500]}"
            )
            content = {"raw": response.text}

        logger.debug(
            f"Centreon API Response: {response.status_code}\n"
            f"Content: {json.dumps(content, indent=2)}"
        )
        response.raise_for_status()
        return content

    except HTTPStatusError as e:
        status = e.response.status_code
        url = str(e.request.url)
        error = CentreonAPIError(status, url, method, content)
        logger.error(error)
        raise error from e
