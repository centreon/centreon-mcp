from fastmcp import FastMCP

from centreon_mcp.types.comment import Comment, CommentResource
from centreon_mcp.utils import logger

comment = FastMCP()


@comment.tool(
    annotations={
        "title": "Add comments on resources (hosts and services) in real-time monitoring",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def add_comments(resources: list[CommentResource]) -> bool:
    """
    Add comments on resources (hosts and services) in real-time monitoring.
    Use `list_resources` tools first to get the resource IDs.
    """
    logger.info("Executing tool add_comments")
    return await Comment.add(resources)
