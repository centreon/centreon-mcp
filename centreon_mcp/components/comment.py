from datetime import UTC, datetime
from typing import Literal

from fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationInfo, field_validator

from centreon_mcp.utils.type import Comment

comment = FastMCP()


class Resource(BaseModel):
    type: Literal["host", "service"]
    id: int = Field(..., description="ID of the resource (host or service)")
    parent_id: int | None = Field(
        ...,
        description="ID of the parent resource (host for service, None for host)",
    )
    comment: str
    date: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))

    @field_validator("parent_id", mode="after")
    @classmethod
    def set_parent_id_for_host(
        cls, value: int | None, info: ValidationInfo
    ) -> int | None:
        if info.data["type"] == "host":
            return info.data["id"]
        else:
            return value


@comment.tool(
    annotations={
        "title": "Add comments on resources in real-time monitoring",
        "readOnlyHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def add_comments(resources: list[Resource]) -> bool:
    """
    Add comments on resources in real-time monitoring.
    Use `list_hosts` and `list_services` tools first to get the resource IDs.
    """
    await Comment.add(
        [
            {
                "parent": {"id": resource.parent_id},
                **resource.model_dump(mode="json", exclude=["parent_id"]),
            }
            for resource in resources
        ]
    )
    return True
