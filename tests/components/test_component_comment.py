from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.comment import (
    set_comments,
)
from centreon_mcp.types.monitoring.comment import CommentParams
from centreon_mcp.utils.base import BaseResource

MODULE = "centreon_mcp.components.comment"


@patch(f"{MODULE}.Comment.set", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_set_comments(logger: MagicMock, comment_set: AsyncMock):

    # Setup args
    params = CommentParams(comment="comment")
    resources = [BaseResource.model_construct()]

    # Mock logger
    logger.info.return_value = None

    # Mock Comment.set
    comment_set.return_value = True

    # Call test function
    result = await set_comments(params, resources)

    # Assert Comment.set called with right args
    comment_set.assert_awaited_once_with(params, resources)

    # Assert result
    assert result
