import re
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from centreon_mcp.auth import Role
from centreon_mcp.components.prompts.diagnosis import host_diagnosis
from centreon_mcp.components.tools import tools


@pytest.mark.parametrize(
    "tool",
    [
        "list_configurations",
        "list_monitoring_resources",
        "count_monitoring_resources_by_status",
        "get_service_metrics",
        "get_service_timeline",
        "get_host_timeline",
        "list_monitoring_actions",
        "list_monitoring_entities",
        "set_monitoring_actions",
        "cancel_monitoring_actions",
        "create_configuration",
        "update_configuration",
        "delete_configurations",
        "manage_monitoring_server_configurations",
    ],
)
@patch("centreon_mcp.auth.plugin", new_callable=MagicMock, create=True)
async def test_host_diagnosis(plugin: MagicMock, tool: str):

    # Mock plugin.role so that every tool is listed
    plugin.role = AsyncMock(return_value=Role.ADMIN)

    # Call test function
    prompt = host_diagnosis("srv-01")

    # Assert the tool exists on the server and is referenced in the prompt
    assert tool in [t.name for t in await tools.list_tools()], f"Tool {tool} not on the server"
    assert re.search(rf"\b{tool}\b", prompt), f"Tool {tool} missing from the prompt"

    # Assert the host name is interpolated and no placeholder is left
    assert '"srv-01"' in prompt
    assert "{host_name}" not in prompt
