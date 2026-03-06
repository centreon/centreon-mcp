from fastmcp import FastMCP

from centreon_mcp.utils import logger
from centreon_mcp.utils.type import Comment, CommentResource

comment = FastMCP()


@comment.tool(
    annotations={
        "title": "Add comments on resources (hosts and services) in real-time monitoring",
        "readOnlyHint": False,
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
    await Comment.add(resources)
    return True
