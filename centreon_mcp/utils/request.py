import json
from copy import deepcopy

import httpx
from fastmcp.server.dependencies import get_http_headers
from httpx import AsyncClient

from centreon_mcp import CREDENTIALS
from centreon_mcp.utils import logger


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
    method: str,
    endpoint: str,
    payload: dict | None = None,
    params: dict | None = None,
    timeout: float | None = None,
) -> dict:
    """
    Make request to Centreon API.
    """
    # Build request arguments
    base = CREDENTIALS["CENTREON_BASE_URL"]
    token = get_http_headers().get("centreon-api-token")
    url = f"{base}/api/latest/{endpoint}"
    headers = {"X-AUTH-TOKEN": token} if token else None

    # Make request and handle response
    try:
        logger.debug(
            f"Centreon API Request: {method} {url}\n"
            f"Headers: {json.dumps(hide(headers), indent=2)}\n"
            f"Params: {json.dumps(params, indent=2)}\n"
            f"Payload: {json.dumps(payload, indent=2)}"
        )
        async with AsyncClient() as client:
            response = await client.request(
                method,
                url,
                headers=headers,
                json=payload,
                params=params,
                timeout=timeout,
            )
            content = response.json() if response.status_code != 204 else {}

            logger.debug(
                f"Centreon API Response: {response.status_code}\n"
                f"Content: {json.dumps(content, indent=2)}"
            )
            response.raise_for_status()
            return content

    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        url = str(e.request.url)
        raise CentreonAPIError(status, url, method, content)
