from datetime import UTC, datetime
from typing import ClassVar

from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseResource
from centreon_mcp.utils.mixins import SetMixin
from centreon_mcp.utils.request import request


class CommentParams(BaseModel):
    comment: str
    date: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))


class Comment(BaseModel, SetMixin[CommentParams]):
    endpoint: ClassVar[str] = "monitoring/resources/comments"
    model_type: ClassVar[str] = "comment"

    @classmethod
    async def set(cls, params: CommentParams, resources: list[BaseResource]) -> bool:
        """
        Create a comment on multiple resources.
        Return True if successful; otherwise, raise an exception.
        """
        payload = {
            "resources": [
                {
                    **params.model_dump(mode="json", exclude_none=True, exclude={"model_type"}),
                    **resource.dump(),
                }
                for resource in resources
            ]
        }
        await request("POST", cls.endpoint, payload=payload)
        return True
