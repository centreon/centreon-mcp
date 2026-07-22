# Centreon MCP Server

This project offers an MCP server for Centreon. Built in Python with the [FastMCP](https://gofastmcp.com/getting-started/welcome) library, it enables users to perform operations on a Centreon instance using natural language commands.

## Features

The MCP server currently exposes 21 tools organized across six functional areas.

### Resource Monitoring

- **list_resources** is the central tool for querying your real-time monitoring data. It supports rich filtering across multiple dimensions simultaneously:
- **By resource type**: filter on hosts only, services only, or both
- **By status**: filter on OK, WARNING, CRITICAL, UNKNOWN, or PENDING states
- **By status type**: distinguish between HARD and SOFT states
- **By name, alias, or parent name**: substring matching on resource identifiers
- **By output/information content**: find resources whose check output contains (or does not contain) a given string — ideal for surfacing specific error messages across your infrastructure
- **By scope**: filter by host group, service group, host category, service category, or monitoring server (poller)
- **Pagination and sorting**: results are paginated and sortable by host name, alias, address, or state

This combination of filters makes it possible to ask highly specific questions such as "Show me all CRITICAL services on hosts in the 'production' host group whose output mentions 'disk full'" and get precise, actionable results directly in the conversation.

Two dedicated counting tools provide a fast status summary without retrieving individual resources:

- **count_hosts_by_status** — returns the total number of hosts in each state (UP, DOWN, UNREACHABLE, PENDING), optionally scoped to one or more host groups or host categories
- **count_services_by_status** — returns the total number of services in each state (OK, WARNING, CRITICAL, UNKNOWN, PENDING), optionally scoped by host name, host group, host category, service group, or service category

Both tools accept multiple filter sets combined with OR logic, making it straightforward to answer questions like "How many hosts are DOWN across the 'production' and 'staging' groups?" in a single call.

A dedicated tool lets the assistant inspect what happened on a single resource:

- **get_host_timeline / get_service_timeline**: fetch the event history of one host or service in real-time monitoring (state changes, notifications, downtimes, acknowledgements, comments). Filterable by event type, content substring and date range. Sorted by date descending by default. Useful to answer "what happened on this resource recently ?" without leaving the conversation.

A dedicated tool lets the assistant refresh state on demand:

- **request_check** — Trigger a check on one or more resources (hosts and services) without waiting for the next polling cycle. Useful right after a remediation action to confirm recovery in conversation. The `is_forced` flag (default `true`) controls whether the configured check interval is bypassed.

### Infrastructure Inventory

A generic tool lets AI assistants explore your monitoring topology:

- **list_monitoring_entities** — List host groups, service groups, or monitoring servers (pollers) by selecting the entity via `model_type`. Host groups and service groups are filterable by host, service, host group, or poller attributes; monitoring servers by name, ID, or running status.

This tool serves as a natural building block: an AI assistant can look up the relevant groups and pollers first, then use those identifiers to scope its subsequent queries precisely.

Two additional tools manage the configuration lifecycle of monitoring servers (pollers):

- **generate_monitoring_servers_configurations** — Generate the configuration files for one or more pollers by their IDs. If no IDs are provided, generates configurations for all pollers. Runs concurrently when multiple IDs are given.
- **reload_monitoring_servers_configurations** — Reload the configuration of one or more pollers by their IDs, pushing the generated files to the monitoring engines. If no IDs are provided, reloads all pollers. Runs concurrently when multiple IDs are given.

Poller configurations can be listed using **list_configurations** with `model_type` set to `monitoring_server` (see [Configuration](#configuration) below).

These tools are typically chained: after modifying host or service configurations, an AI assistant can generate then reload the affected pollers to apply changes without leaving the conversation.

### Configuration

Four generic tools cover the full configuration lifecycle for hosts, host groups, host categories, host severities, host templates, and commands. Each tool accepts a `model_type` parameter to select the entity to operate on.

- **list_configurations** — List configurations, filterable by entity-specific fields (ID, name, alias, address, activation status, etc.). Results are paginated and sortable. Supported entity types: `command`, `host`, `host_category`, `host_group`, `host_severity`, `host_template`, `monitoring_server`.
- **create_configuration** — Create a new configuration by providing the required and optional parameters for the chosen entity type. Supported entity types: `command`, `host`, `host_category`, `host_group`, `host_severity`, `host_template`.
- **update_configuration** — Partially update an existing configuration by ID, using only the fields that need to change. Supported entity types: `host`, `host_category`, `host_group`, `host_severity`, `host_template`.
- **delete_configurations** — Delete one or more configurations by their IDs. Supported entity types: `host`, `host_category`, `host_group`, `host_severity`, `host_template`.

Each entity type carries its own set of parameters passed alongside `model_type`. For example, creating a host requires specifying the monitoring server, name, and IP address, and accepts optional parameters such as SNMP community and version, geographic coordinates, severity, check and event handler commands, notification options, flap detection thresholds, and host group/category/template associations.

### Acknowledgements

Acknowledge alerts without ever leaving your conversation:

- **list_acknowledgements** — List current acknowledgements, with pagination and sorting (by ID, host, start time, entry time, etc.)
- **set_acknowledgements** — Acknowledge one or more resources at once, applying a message and configuring options such as sticky acknowledgement and notifications
- **cancel_acknowledgements** — Remove acknowledgements from one or more resources, with the option to also cancel service acknowledgements when a host is unacknowledged

### Downtimes

Full downtime lifecycle management through conversation:

- **list_downtimes** — Query scheduled or active downtimes, filterable by host name, alias, address, state, poller, and downtime properties (fixed, cancelled)
- **set_downtimes** — Schedule a downtime on one or more hosts or services, specifying start and end times, a comment, and whether the downtime is fixed or flexible
- **cancel_downtimes** — Cancel one or more downtimes by their IDs

### Comments

- **set_comments** — Attach a comment to any host or service in real-time monitoring, useful for leaving context notes on an ongoing incident directly from the AI assistant

### Metrics

- **get_service_metrics** — Retrieve all metrics of a service with their current values, units, and warning/critical thresholds. Useful for answering questions like "what is the current CPU usage?" or "how close is disk usage to the critical threshold?" without leaving the conversation.

## Quick Start

1. Clone the repository

```shell
git clone https://github.com/centreon/centreon-mcp.git
cd centreon-mcp
```

2. Ensure all required environment variables are set. Default values are used for optional variables.

| Name                     | Default | Description                                           |
| ------------------------ | ------- | ----------------------------------------------------- |
| `CENTREON_BASE_URL`      |         | Base URL of the Centreon instance.                    |
| `CENTREON_MCP_PORT`      | `8000`  | Port used to start the Centreon MCP service.          |
| `CENTREON_MCP_LOG_LEVEL` | `INFO`  | Minimal severity level for Centreon MCP service logs. |

### Using UV

3. Install dependencies and synchronize

```shell
uv sync
```

4. Start the MCP server

```shell
uv run centreon-mcp-server
```

5. If the MCP server is not reachable from the internet, expose it using a tunneling tool such as [Ngrok](https://ngrok.com):

```shell
ngrok http 8000
```

> Replace `8000` with the value of `CENTREON_MCP_PORT` if you changed the default.

### Using Docker

3. Build Docker image

```shell
docker build -t centreon/mcp .
```

4. Start the MCP server

```shell
docker compose up
```

5. To make it reachable from the internet, export `NGROK_AUTHTOKEN` in the environment and enable `ngrok` profile.

```shell
docker compose --profile ngrok up
```

> Use `curl http://localhost:4040/api/tunnels` to retrieve public URL

## Integration

<details>
<summary>ChatGPT</summary>

1. Open [ChatGPT](https://chatgpt.com) and sign in.
2. Click on your profile picture in the bottom-left corner, then select **Settings**.
3. Go to the **Connectors** section and click **Create**.
4. Fill in the form:
   - **Name**: `Centreon` (or any name you prefer)
   - **URL**: the address of your running MCP server, e.g. `https://<ngrok-subdomain>.ngrok-free.app/mcp`
   - **Headers**: Add valid Centreon API token in headers under field `centreon-api-token`
5. Click **Save** to register the connector.

Once the connector is added, ChatGPT will automatically discover and use the Centreon MCP tools in your conversations.

</details>

<details>
<summary>Mistral Le Chat</summary>

1. Open [Le Chat](https://chat.mistral.ai) and sign in.
2. Click on **Intelligence** in the left sidebar, then select **Connectors**.
3. Click **Add a connector**, then choose **Custom MCP connector**.
4. Fill in the form:
   - **Name**: `Centreon` (or any name you prefer)
   - **URL**: the address of your running MCP server, e.g. `https://<ngrok-subdomain>.ngrok-free.app/mcp`
   - **Headers**: Add valid Centreon API token in headers under field `centreon-api-token`
5. Click **Save** to register the connector.

Once the connector is added, Le Chat will automatically discover and use the Centreon MCP tools in your conversations.

</details>

<details>
<summary>Claude Code</summary>

Register your MCP server using the HTTP transport with the local address and Centreon API token in headers

```shell
claude mcp add -t http centreon http://localhost:8000/mcp -H "centreon-api-token: <token>"
```

> Replace `8000` with the value of `CENTREON_MCP_PORT` if you changed the default.

List configured MCP servers and confirm `centreon` is present:

```shell
/mcp list
```

</details>
