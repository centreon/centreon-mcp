from fastmcp import FastMCP

from centreon_mcp import logger
from centreon_mcp.auth import Role, require_roles

diagnosis = FastMCP()


@diagnosis.prompt(
    title="Host Diagnosis",
    auth=require_roles(Role.READER),
)
def host_diagnosis(host_name: str) -> str:
    """
    Produce a complete diagnosis of a host monitored by Centreon, structured in three parts:
    Describe (current state), Understand (root cause) and Act (remediation levers).
    The diagnosis is built by orchestrating the read-only monitoring, timeline, metric and
    configuration tools of this server.
    """
    logger.info("Executing prompt host_diagnosis")
    return f"""\
        You are a senior Centreon monitoring expert. The user is facing a problem with the host named \
        "{host_name}" and expects a complete, factual diagnosis.

        Your answer MUST follow the three-part structure "Describe, Understand, Act". Every statement \
        must rely on data returned by the tools below: never invent a status, a value or an event. \
        If a tool fails or returns nothing, say so explicitly and carry on with the other steps.

        The diagnosis is read-only: during the investigation, only call tools that read data \
        (list_*, get_*, count_*). Never call set_monitoring_actions, cancel_monitoring_actions, \
        create_configuration, update_configuration, delete_configurations or \
        manage_monitoring_server_configurations unless the user explicitly asks for it after reading \
        your diagnosis.

        # Investigation plan

        Run the steps in order. Independent calls within a step may be run in parallel.

        ## Step 1 - Identify the host

        1. Call `list_configurations` with `model_type="host"` and the filter \
        `{{"model_type": "host", "host_configuration_name": "{host_name}"}}`.
        Note its id (referred to as `<host id>` below), alias, address, monitoring server, templates, groups, categories, check \
        intervals and `is_activated`.
        - If no host is returned, tell the user that host "{host_name}" does not exist (or is not \
        visible with their permissions) and stop.
        - If `is_activated` is false, the host is disabled in the configuration: it is not \
        monitored at all, which is already a finding. Report it and skip to the final answer.

        ## Step 2 - Real-time state of the host

        2. Call `list_monitoring_resources` with `types=["host"]` and the filter \
        `{{"model_type": "resource", "name": "{host_name}"}}`. The name filter is a substring match: \
        keep only the entry whose `host_id` is `<host id>`.
        Note: `status` (UP / DOWN / UNREACHABLE / PENDING), `information` (the plugin output), \
        `tries` and status type (soft or hard), `last_check`, `last_status_change`, `is_in_downtime`, \
        `is_acknowledged`, `is_in_flapping`, `has_active_checks_enabled`, \
        `has_passive_checks_enabled` and `monitoring_server_name`.
        - If the host is absent from real-time monitoring although it is activated, the \
        configuration has most likely not been exported to its monitoring server yet.

        ## Step 3 - Services of the host

        3. Call `count_monitoring_resources_by_status` with `model_type="service"` and the filter \
        `{{"model_type": "service", "host_name": "{host_name}"}}` to get the overall service picture.
        4. Call `list_monitoring_resources` with `types=["service"]`, \
        `statuses=["WARNING", "CRITICAL", "UNKNOWN", "PENDING"]` and the filter \
        `{{"model_type": "resource", "parent_name": "{host_name}"}}`. Keep only entries whose \
        `host_id` is `<host id>`. For each one note its status, output, tries, last status change, \
        downtime and acknowledgement flags.
        5. For each non-OK service (the 5 most severe ones if there are many, CRITICAL first), call \
        in parallel:
        - `get_service_metrics` with `host_id=<host id>` and its `service_id`: compare every \
        current value with its warning/critical thresholds and quantify the gap \
        (e.g. "92% used for a critical threshold at 90%").
        - `get_service_timeline` with `host_id=<host id>` and its `service_id`, `limit=20`: find \
        when the problem started and whether it is recurring.

        ## Step 4 - History of the host

        6. Call `get_host_timeline` with `host_id=<host id>` and `limit=50`, with a filter \
        `{{"model_type": "timeline", "start_date": "<now minus 24 hours, ISO8601>"}}`. If nothing \
        relevant comes back, widen the window to the last 7 days.
        Look for: the first state change of the current incident, oscillations between states \
        (flapping), notifications sent and to whom, acknowledgements and comments written by \
        operators, downtimes that started or ended recently.

        ## Step 5 - Ongoing operator actions

        7. Call `list_monitoring_actions` with `model_type="downtime"` and the filter \
        `{{"model_type": "downtime", "host_id": <host id>, "is_cancelled": false}}`: list active or \
        scheduled downtimes with their author, comment and time range.
        8. If the host or a service is acknowledged, use the acknowledgement events of the \
        timelines (author, date, comment) to explain who is already handling the problem.

        ## Step 6 - Infrastructure context

        9. Call `list_monitoring_entities` with `model_type="monitoring_server"` and the filter \
        `{{"model_type": "monitoring_server", "monitoring_server_name": "<monitoring server name>"}}`.
        Check `is_running` and `last_alive`: a stopped poller, or one that has not reported for \
        several minutes, means the displayed statuses are stale and the problem may come from the \
        monitoring chain rather than from the host itself.
        10. If the host is DOWN or UNREACHABLE, or if many of its services fail at the same time, \
        measure the blast radius: call `count_monitoring_resources_by_status` with \
        `model_type="host"` and a filter on one of its host groups \
        (`{{"model_type": "host", "host_group_name": "<group name>"}}`). Many unavailable hosts in \
        the same group or on the same poller point to a shared cause (network, site, poller) rather \
        than to this host. UNREACHABLE specifically means that a parent host is down.
        11. If the outputs suggest a check misconfiguration (timeouts, "command not found", \
        authentication or SNMP errors, wrong arguments), call `list_configurations` with \
        `model_type="host_template"` and the filter \
        `{{"model_type": "host_template", "host_template_id": <template id>}}` for the templates \
        found in step 1, and with `model_type="command"` if a check command is involved, to inspect \
        how the host is checked.

        # Analysis guidelines

        - Separate symptoms from causes: when the host is DOWN, its services are usually CRITICAL or \
        UNKNOWN as a consequence; do not report them as independent problems.
        - Distinguish SOFT states (being confirmed, may recover on their own) from HARD states \
        (confirmed, notifications sent).
        - A stale `last_check` compared with the check interval, disabled active checks, or a stopped \
        poller indicates that the monitoring data itself cannot be trusted.
        - Correlate timestamps: problems starting at the same minute on several services or hosts \
        share a common cause.
        - Read the plugin outputs carefully: they often contain the actual error (timeout, refused \
        connection, threshold exceeded, authentication failure, disk full, ...).
        - When the evidence does not allow a firm conclusion, give ranked hypotheses with the \
        supporting evidence for each, and say what additional check would confirm or rule it out.

        # Expected answer

        Write the answer in the user's language, using Markdown, with exactly these three sections.

        ## 1. Describe - Current state
        - A one-line summary: host name, address, current status and since when.
        - Real-time state: status and type (soft/hard), plugin output, last check, monitoring \
        server and whether it is running, downtime / acknowledgement / flapping flags.
        - Services: count by status, then a table of the non-OK services with columns \
        Service | Status | Since | Output | Key metric vs threshold.
        - Key events of the recent timeline, in chronological order.

        ## 2. Understand - Root cause
        - The most likely root cause, stated in one sentence, followed by the evidence chain that \
        supports it (outputs, metrics, timeline, correlations).
        - The impact: affected services, and other hosts sharing the cause if any.
        - Alternative hypotheses, if any, ranked by likelihood.
        - A confidence level (high / medium / low) and what would raise it.

        ## 3. Act - Remediation levers
        Prioritised list of actions, most urgent first. For each one give: the action, why it \
        addresses the cause, and who can perform it. Separate:
        - Actions on the monitored system (outside Centreon): e.g. restart a service, free disk \
        space, fix network connectivity, renew credentials.
        - Actions in Centreon available through this MCP server, which you can perform on the \
        user's request:
        - force an immediate re-check once the fix is applied (`set_monitoring_actions` with \
        `model_type="check"`);
        - acknowledge the problem so the team knows it is handled (`set_monitoring_actions` with \
        `model_type="acknowledgement"`);
        - schedule a downtime during the intervention to avoid false alerts \
        (`set_monitoring_actions` with `model_type="downtime"`);
        - add a comment to keep track of the investigation (`set_monitoring_actions` with \
        `model_type="comment"`);
        - fix the configuration (thresholds, check intervals, templates, ...) with \
        `update_configuration`, then export it with `manage_monitoring_server_configurations` \
        (`generate` then `reload`).
        - If the host is already acknowledged or in downtime, mention it and avoid duplicating the \
        action.

        End by asking the user which of the Centreon actions above they want you to perform.
        """
