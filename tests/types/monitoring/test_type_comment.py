from unittest.mock import AsyncMock, patch

from centreon_mcp.types.monitoring.comment import Comment, CommentParams
from centreon_mcp.utils.base import BaseResource

MODULE = "centreon_mcp.types.monitoring.comment"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_set_comment(request: AsyncMock):

    # Setup args
    params = CommentParams(comment="comment")
    resources = [BaseResource(host_id=10, type="host", resource_id=10)]

    # Mock request
    request.return_value = None

    # Call test function
    await Comment.set(params, resources)

    # Assert request called with right args
    payload = {
        "resources": [
            {
                "type": "host",
                "id": 10,
                "parent": {"id": 10},
                **params.model_dump(mode="json", exclude={"model_type"}),
            }
        ]
    }
    request.assert_awaited_once_with("POST", "monitoring/resources/comments", payload=payload)
