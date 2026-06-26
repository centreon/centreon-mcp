from unittest.mock import AsyncMock, patch

from centreon_mcp.types.monitoring.comment import Comment, CommentResource

MODULE = "centreon_mcp.types.monitoring.comment"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_add_comment(request: AsyncMock):

    # Setup args
    resources = [CommentResource.model_construct(host_id=10)]

    # Mock request
    request.return_value = None

    # Call test function
    await Comment.add(resources)

    # Assert request called with right args
    payload = {"resources": [resource.dump() for resource in resources]}
    request.assert_awaited_once_with("POST", "monitoring/resources/comments", payload=payload)
