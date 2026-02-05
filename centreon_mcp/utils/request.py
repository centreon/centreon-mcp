import httpx

from centreon_mcp import CREDENTIALS
from centreon_mcp.utils.logger import logger


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
    json: dict | None = None,
    params: dict | None = None,
    timeout: float | None = None,
) -> dict:
    """
    Make request to Centreon API.
    """
    # Build request arguments
    base = CREDENTIALS["CENTREON_BASE_URL"]
    token = CREDENTIALS["CENTREON_API_TOKEN"]
    url = f"{base}/api/latest/{endpoint}"
    headers = {"X-AUTH-TOKEN": token}

    # Make request and handle response
    try:
        logger.debug(
            f"Centreon API Request: {method} {url} "
            f"Headers: {headers} JSON: {json} Params: {params}"
        )
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method, url, headers=headers, json=json, params=params, timeout=timeout
            )
            content = response.json()
            logger.debug(f"Centreon API Response: {content}")
            response.raise_for_status()
            return content

    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        url = str(e.request.url)
        raise CentreonAPIError(status, url, method, content)
