from unittest.mock import MagicMock, patch

from centreon_mcp import CREDENTIALS
from centreon_mcp.__main__ import main

MODULE = "centreon_mcp.__main__"


@patch(f"{MODULE}.mcp")
def test_main(mcp: MagicMock):

    # Mock mcp.run
    mcp.run.return_value = None

    # Call test function
    main()

    # Assert mcp.run called with rigt args
    host = CREDENTIALS["CENTREON_MCP_HOST"]
    port = int(CREDENTIALS["CENTREON_MCP_PORT"])
    mcp.run.assert_called_once_with(transport="http", host=host, port=port)
