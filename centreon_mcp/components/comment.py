from fastmcp import FastMCP

from centreon_mcp.types.monitoring.comment import Comment, CommentParams
from centreon_mcp.utils import logger
from centreon_mcp.utils.base import BaseResource

comment = FastMCP()


@comment.tool(
    annotations={
        "title": "Set comments on resources (hosts and services) in real-time monitoring",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def set_comments(params: CommentParams, resources: list[BaseResource]) -> bool:
    """
    Set comments on resources (hosts and services) in real-time monitoring.
    Use `list_resources` tools first to get the resource IDs.
    """
    logger.info("Executing tool set_comments")
    return await Comment.set(params, resources)
