# Centreon MCP Server

This project offers an MCP server for Centreon. Built in Python with the [FastMCP](https://gofastmcp.com/getting-started/welcome) library, it enables users to perform operations on a Centreon instance using natural language commands.

## Features

The MCP server currently exposes 37 tools organized across eleven functional areas.

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

Three read-only tools allow AI assistants to explore your monitoring topology:

- **list_hostgroups** — List host groups, filterable by host name, alias, address, state, poller, or group ID
- **list_servicegroups** — List service groups, filterable by host, service, host group, or poller attributes
- **list_monitoring_servers** — List pollers, with the ability to filter by name, ID, or running status

These tools serve as natural building blocks: an AI assistant can look up the relevant groups and pollers first, then use those identifiers to scope its subsequent queries precisely.

### Host Configuration

Full host configuration lifecycle management through conversation:

- **list_host_configurations** — List host configurations, filterable by ID, name, address, poller, host group, host category, and activation status. Results are paginated and sortable by name, alias, or address.
- **create_host_configuration** — Create a new host configuration by specifying the monitoring server, name, and IP address. Supports a wide range of optional parameters: SNMP community and version, geographic coordinates, severity, check and event handler commands with arguments, check interval settings, notification options, flap detection thresholds, freshness checking, and host group/category/template associations.
- **update_host_configuration** — Partially update an existing host configuration by ID, using the same parameter set as creation.
- **delete_host_configurations** — Delete one or more host configurations by their IDs.

### Host Severities

Manage host severity levels used to prioritize hosts in your monitoring:

- **list_host_severities** — List host severities, filterable by ID, name, alias, level range, and activation status. Results are paginated and sortable by name, alias, or level.
- **create_host_severity** — Create a new host severity by specifying a name, level, and icon ID. An alias is optional.
- **delete_host_severities** — Delete one or more host severities by their IDs.

### Host Group Configuration

Full host group configuration lifecycle management through conversation:

- **list_hostgroup_configurations** — List host group configurations, filterable by ID, name, alias, and activation status. Results are paginated and sortable by id, name, alias, or activation status.
- **create_host_group_configuration** — Create a new host group configuration by specifying its name.
- **update_host_group_configuration** — Partially update an existing host group configuration by ID.
- **delete_host_group_configurations** — Delete one or more host group configurations by their IDs.

### Host Category Configuration

Full host category configuration lifecycle management through conversation:

- **list_host_category_configurations** — List host category configurations, filterable by ID, name, alias, and activation status. Results are paginated and sortable by id, name, alias, or activation status.
- **create_host_category_configuration** — Create a new host category configuration by specifying its name and alias. Supports an optional comment and activation status.
- **update_host_category_configuration** — Partially update an existing host category configuration by ID.
- **delete_host_category_configurations** — Delete one or more host category configurations by their IDs.

### Host Template Configuration

Full host template configuration lifecycle management through conversation:

- **list_host_templates** — List host templates, filterable by ID, name, alias, and locked status. Results are paginated and sortable by name, alias, or address.
- **create_host_template** — Create a new host template by specifying a name and alias. Supports a wide range of optional parameters: SNMP community and version, severity, check and event handler commands with arguments, check interval settings, notification options, flap detection thresholds, freshness checking, and category associations.
- **update_host_template** — Partially update an existing host template by ID, using the same parameter set as creation.
- **delete_host_templates** — Delete one or more host templates by their IDs.

### Acknowledgements

Acknowledge alerts without ever leaving your conversation:

- **list_acknowledgements** — List current acknowledgements, with pagination and sorting (by ID, host, start time, entry time, etc.)
- **add_acknowledgements** — Acknowledge one or more resources at once, applying a message and configuring options such as sticky acknowledgement and notifications
- **cancel_acknowledgements** — Remove acknowledgements from one or more resources, with the option to also cancel service acknowledgements when a host is unacknowledged

### Downtimes

Full downtime lifecycle management through conversation:

- **list_downtimes** — Query scheduled or active downtimes, filterable by host name, alias, address, state, poller, and downtime properties (fixed, cancelled)
- **set_downtimes** — Schedule a downtime on one or more hosts or services, specifying start and end times, a comment, and whether the downtime is fixed or flexible
- **cancel_downtimes** — Cancel one or more downtimes by their IDs

### Commands

Manage check, notification, discovery, and miscellaneous commands from within the conversation:

- **list_commands** — List commands, filterable by ID, name, type (CHECK, NOTIFICATION, MISCELLANEOUS, DISCOVERY), or locked status. Results are paginated and sortable by name.
- **add_command** — Create a new command by specifying its name, type, and command line. Supports optional shell mode, argument descriptions, macro descriptions, a connector, and a graph template.

### Comments

- **add_comments** — Attach a comment to any host or service in real-time monitoring, useful for leaving context notes on an ongoing incident directly from the AI assistant

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
