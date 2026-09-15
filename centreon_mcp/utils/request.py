import json
from copy import deepcopy
from typing import Any

from fastmcp.server.dependencies import get_access_token
from httpx import AsyncClient, HTTPStatusError

from centreon_mcp.auth.base import Tenant
from centreon_mcp.utils import logger

client: AsyncClient | None = None


# Redacted in both directions: requests carry credentials, responses carry tokens
SECRET_FIELDS = frozenset(
    {
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
    }
)

REDACTED = "[redacted]"


def hide(headers: dict | None) -> dict | None:
    """
    Hide Centreon API token in headers for logging
    """
    if headers is None:
        return None

    hidden = deepcopy(headers)
    token = headers.get("X-AUTH-TOKEN")
    if token is None:
        return hidden

    # Keeping a tail to recognise the token only works while there is more to hide than to keep:
    # a short one would otherwise be written out whole
    size = 6
    hidden["X-AUTH-TOKEN"] = (
        (len(token) - size) * "*" + token[-size:] if len(token) > 2 * size else REDACTED
    )
    return hidden


def secret(key: object, data: dict) -> bool:
    """
    Tell whether a key of a Centreon payload holds a credential.

    Macros carry the passwords a monitoring plugin authenticates with, under the neutral key
    `value`; the entity itself says so through `is_password`.
    """
    if str(key).lower() in SECRET_FIELDS:
        return True
    return key == "value" and data.get("is_password") is True


def redact(data: Any) -> Any:
    """
    Return a copy of a payload or a response with every secret replaced.

    Debug logs are shipped off-host and outlive the credentials they would otherwise carry.
    """
    if isinstance(data, dict):
        return {
            key: REDACTED if secret(key, data) else redact(value) for key, value in data.items()
        }
    if isinstance(data, list):
        return [redact(item) for item in data]
    return data


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
    tenant: Tenant | None = None,
) -> dict:
    """
    Make request to Centreon API.

    The Centreon to call is resolved by the authentication plugin, unless an explicit tenant is
    given, which the startup connectivity check relies on to reach each tenant in turn.
    """
    # Check Centreon Client is initialiazed
    if client is None:
        raise RuntimeError("Centreon client is not initialized")

    # Build request arguments
    # Imported late, as a second guard against the cycle described in centreon_mcp/auth/__init__.py
    from centreon_mcp.auth import get_plugin

    tenant = tenant or await get_plugin().tenant(get_access_token())
    token = tenant.token
    url = f"{tenant.base_url}/api/latest/{endpoint}"
    headers = {"X-AUTH-TOKEN": token} if token else None
    params = params or {}
    params = {name: value for name, value in params.items() if value is not None}

    # Make request and handle response
    logger.debug(
        f"Centreon API Request: {method} {url}\n"
        f"Headers: {json.dumps(hide(headers), indent=2)}\n"
        f"Params: {json.dumps(params, indent=2)}\n"
        f"Payload: {json.dumps(redact(payload), indent=2)}"
    )
    try:
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
            f"Content: {json.dumps(redact(content), indent=2)}"
        )
        response.raise_for_status()
        return content

    except HTTPStatusError as e:
        status = e.response.status_code
        url = str(e.request.url)
        error = CentreonAPIError(status, url, method, redact(content))
        logger.error(error)
        raise error from e
