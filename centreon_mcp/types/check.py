from pydantic import BaseModel

from centreon_mcp.types.base import BaseResource
from centreon_mcp.utils.request import request


class CheckResource(BaseResource):
    pass


class Check(BaseModel):
    @staticmethod
    async def request(is_forced: bool, resources: list[CheckResource]) -> None:
        """
        Request a check on multiple resources (hosts and services).
        When `is_forced` is True, the check is executed immediately regardless of
        the configured check interval. Otherwise, the check is scheduled for the
        next available execution slot.
        """
        payload = {
            "check": {"is_forced": is_forced},
            "resources": [resource.dump() for resource in resources],
        }
        await request("POST", "monitoring/resources/check", payload=payload)
