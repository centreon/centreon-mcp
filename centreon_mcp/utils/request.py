import json
from copy import deepcopy

from fastmcp.server.dependencies import get_http_headers
from httpx import AsyncClient, HTTPStatusError

from centreon_mcp import logger, settings

client: AsyncClient | None = None


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
    # Check Centreon Client is initialiazed
    if client is None:
        raise RuntimeError("Centreon client is not initialized")

    # Build request arguments
    token = get_http_headers().get("centreon-api-token") or settings.api_token
    headers = {"X-AUTH-TOKEN": token} if token else None
    params = params or {}
    params = {name: value for name, value in params.items() if value is not None}

    # Make request and handle response
    logger.debug(
        f"Centreon API Request: {method} {endpoint}\n"
        f"Headers: {json.dumps(hide(headers), indent=2)}\n"
        f"Params: {json.dumps(params, indent=2)}\n"
        f"Payload: {json.dumps(payload, indent=2)}"
    )
    try:
        response = await client.request(
            method, endpoint, headers=headers, json=payload, params=params
        )
        try:
            content = response.json() if (response.status_code != 204 and response.content) else {}
        except json.JSONDecodeError:
            logger.warning(
                f"Non-JSON response from {method} {endpoint} (status {response.status_code}): {response.text[:500]}"
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
