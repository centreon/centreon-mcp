from pydantic import BaseModel

from centreon_mcp.types.base import StatusCount
from centreon_mcp.utils.request import request


class ServiceStatusCount(StatusCount):
    critical: int
    unknown: int
    ok: int
    warning: int


class Service(BaseModel):
    @staticmethod
    async def count_by_status(search: str | None) -> ServiceStatusCount:
        """
        Count services by status.
        """
        params = {"search": search}
        content = await request("GET", "monitoring/services/status", params=params)
        return ServiceStatusCount(**content)
