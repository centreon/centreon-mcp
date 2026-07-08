from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseResource
from centreon_mcp.utils.request import request


class CheckResource(BaseResource):
    pass


class CheckParams(BaseModel):
    is_forced: bool = Field(
        True,
        description=(
            "When `is_forced` is True, the check is executed immediately regardless of the configured check interval."
            "Otherwise, the check is scheduled for the next available execution slot.)"
        ),
    )


class Check(BaseModel):
    @staticmethod
    async def request(params: CheckParams, resources: list[CheckResource]) -> bool:
        """
        Request a check on multiple resources (hosts and services).
        Return True if successful; otherwise, raise an exception.
        """
        payload = {
            "check": params.model_dump(mode="json"),
            "resources": [resource.dump() for resource in resources],
        }
        await request("POST", "monitoring/resources/check", payload=payload)
        return True
