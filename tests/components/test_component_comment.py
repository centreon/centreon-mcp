from unittest.mock import AsyncMock, MagicMock, patch

from centreon_mcp.components.comment import (
    add_comments,
)
from centreon_mcp.types.comment import CommentResource

MODULE = "centreon_mcp.components.comment"


@patch(f"{MODULE}.Comment.add", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_add_comments(logger: MagicMock, add: AsyncMock):

    # Setup args
    resources = [CommentResource.model_construct()]

    # Mock logger
    logger.info.return_value = None

    # Mock Comment.add
    add.return_value = True

    # Call test fonction
    result = await add_comments(resources)

    # Assert Comment.add called with right args
    add.assert_awaited_once_with(resources)

    # Assert result
    assert result
