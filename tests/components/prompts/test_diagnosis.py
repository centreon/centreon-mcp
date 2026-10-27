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
def test_host_diagnosis(tool: str):

    # Call test function
    prompt = host_diagnosis("srv-01")

    # Assert the tool is referenced in the prompt
    assert re.search(rf"\b{tool}\b", prompt), f"Tool {tool} missing from the prompt"


def test_host_diagnosis_indentation():

    # Call test function
    prompt = host_diagnosis("srv-01")

    # Assert the code indentation is stripped, so Markdown headings are not read as code blocks
    assert prompt.startswith("You are"), "Prompt starts with stray indentation"
    assert re.search(r"^# Investigation plan$", prompt, re.MULTILINE), "Heading is indented"

    # Assert no line break leaves a run of spaces in the middle of a sentence
    assert not re.search(r"\S {2,}\S", prompt), "Stray spaces inside a line"
