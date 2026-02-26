from datetime import UTC, datetime

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from centreon_mcp.utils.type import Comment, ResourceType

comment = FastMCP()


class Resource(BaseModel):
    type: ResourceType
    resource_id: int = Field(..., serialization_alias="id")
    host_id: int
    comment: str
    date: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))


@comment.tool(
    annotations={
        "title": "Add comments on resources (hosts and services) in real-time monitoring",
        "readOnlyHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def add_comments(resources: list[Resource]) -> bool:
    """
    Add comments on resources (hosts and services) in real-time monitoring.
    Use `list_resources` tools first to get the resource IDs.
    """
    await Comment.add(
        [
            {
                "parent": {"id": resource.host_id},
                **resource.model_dump(mode="json", by_alias=True, exclude={"host_id"}),
            }
            for resource in resources
        ]
    )
    return True
