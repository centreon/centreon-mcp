from unittest.mock import MagicMock, patch

from centreon_mcp import settings
from centreon_mcp.__main__ import main

MODULE = "centreon_mcp.__main__"


@patch(f"{MODULE}.mcp")
def test_main(mcp: MagicMock):

    # Mock mcp.run
    mcp.run.return_value = None

    # Call test function
    main()

    # Assert mcp.run called with rigt args
    mcp.run.assert_called_once_with(
        transport="http", host=settings.mcp_host, port=settings.mcp_port
    )
