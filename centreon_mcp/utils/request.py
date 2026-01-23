import httpx

from centreon_mcp import CREDENTIALS


class CentreonAPIError(Exception):
    """
    Custom exception for Centreon API errors.
    """

    pass


async def request(
    method: str,
    endpoint: str,
    data: dict | None = None,
    params: dict | None = None,
    timeout: float | None = None,
) -> dict:
    """
    Make request to Centreon API.
    """
    # Build request arguments
    host = CREDENTIALS["CENTREON_HOST"]
    port = CREDENTIALS["CENTREON_PORT"]
    token = CREDENTIALS["CENTREON_API_TOKEN"]
    url = f"http://{host}:{port}/centreon/api/latest/{endpoint}"
    headers = {"X-AUTH-TOKEN": token}

    # Make request and handle response
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method, url, headers=headers, data=data, params=params, timeout=timeout
            )
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError):
        raise CentreonAPIError()
