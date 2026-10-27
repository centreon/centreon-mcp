import re

import pytest

from centreon_mcp.components.prompts.diagnosis import host_diagnosis

MODULE = "centreon_mcp.components.prompts.diagnosis"


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
async def test_host_diagnosis(tool: str):

    # Call test function
    prompt = host_diagnosis("srv-01")

    # Assert the tool is referenced in the prompt
    assert re.search(rf"\b{tool}\b", prompt), f"Tool {tool} missing from the prompt"
