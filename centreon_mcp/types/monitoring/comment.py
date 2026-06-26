from datetime import UTC, datetime

from pydantic import BaseModel, Field

from centreon_mcp.types.base import BaseResource
from centreon_mcp.utils.request import request


class CommentResource(BaseResource):
    comment: str
    date: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))


class Comment(BaseModel):
    @staticmethod
    async def add(resources: list[CommentResource]) -> bool:
        """
        Add comments on multiple resources.
        Return True if successful; otherwise, raise an exception.
        """
        payload = {"resources": [resource.dump() for resource in resources]}
        await request("POST", "monitoring/resources/comments", payload=payload)
        return True
