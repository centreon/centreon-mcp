# Centreon MCP Server

This project offers an MCP server for Centreon. Built in Python with the [FastMCP](https://gofastmcp.com/getting-started/welcome) library, it enables users to perform operations on a Centreon instance using natural language commands.

## Features

The MCP server currently exposes 16 tools organized across five functional areas.

### Resource Monitoring

| Tool                        | Types             | Description                                                                                                                                           |
| --------------------------- | ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `list_monitoring_resources` | `host` `service` | Query real-time monitoring data with rich filtering (status, status type, name/alias, output content, scope), paginated and sortable.                 |
| `count_hosts_by_status`     | `host`            | Return the total number of hosts in each state (UP, DOWN, UNREACHABLE, PENDING), optionally scoped by host group or host category.                    |
| `count_services_by_status`  | `service`         | Return the total number of services in each state (OK, WARNING, CRITICAL, UNKNOWN, PENDING), optionally scoped by host, host group, or service group. |
| `get_host_timeline`         | `host`            | Fetch a host's event history (state changes, notifications, downtimes, acknowledgements, comments), filterable and sorted by date.                    |
| `get_service_timeline`      | `service`         | Fetch a service's event history (state changes, notifications, downtimes, acknowledgements, comments), filterable and sorted by date.                 |

`list_monitoring_resources` filters can be combined to ask highly specific questions such as "Show me all CRITICAL services on hosts in the 'production' host group whose output mentions 'disk full'". The two counting tools accept multiple filter sets combined with OR logic, making it straightforward to answer questions like "How many hosts are DOWN across the 'production' and 'staging' groups?" in a single call.

### Infrastructure Inventory

| Tool                                         | Types                                              | Description                                                                                        |
| -------------------------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `list_monitoring_entities`                   | `host_group` `service_group` `monitoring_server` | List host groups, service groups, or monitoring servers (pollers), filterable by their attributes. |
| `generate_monitoring_servers_configurations` | `monitoring_server`                                | Generate the configuration files for one or more pollers (or all pollers if none specified).       |
| `reload_monitoring_servers_configurations`   | `monitoring_server`                                | Reload poller configuration, pushing the generated files to the monitoring engines.                |

`list_monitoring_entities` is a natural building block: an AI assistant can look up the relevant groups and pollers first, then use those identifiers to scope its subsequent queries precisely. Poller configurations can also be listed using `list_configurations` with `model_type` set to `monitoring_server` (see [Configuration](#configuration) below). The generate and reload tools are typically chained: after modifying host or service configurations, an AI assistant can generate then reload the affected pollers to apply changes without leaving the conversation.

### Configuration

| Tool                    | Types                                                                                                                                                                       | Description                                                                          |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `list_configurations`   | `command` `host` `service` `host_category` `host_group` `service_category` `service_group` `host_severity` `host_template` `monitoring_server` | List configurations, filterable by entity-specific fields, paginated and sortable.   |
| `create_configuration`  | `command` `host` `service` `host_category` `host_group` `service_category` `service_group` `host_severity` `host_template`                      | Create a new configuration for the chosen entity type.                               |
| `update_configuration`  | `host` `service` `host_category` `host_group` `host_severity` `host_template`                                                                      | Partially update an existing configuration by ID, using only the fields that change. |
| `delete_configurations` | `host` `service` `host_category` `host_group` `service_category` `service_group` `host_severity` `host_template`                                 | Delete one or more configurations by their IDs.                                      |

Each tool accepts a `model_type` parameter to select the entity to operate on, and each entity type carries its own set of parameters passed alongside `model_type`. For example, creating a host requires specifying the monitoring server, name, and IP address, and accepts optional parameters such as SNMP community and version, geographic coordinates, severity, check and event handler commands, notification options, flap detection thresholds, and host group/category/template associations. Creating a service requires specifying the linked host and a name, and accepts optional parameters such as the service template, check and event handler commands, notification options, flap detection thresholds, and service category/group associations.

### Monitoring Actions

| Tool                        | Types                                             | Description                                                                                                        |
| --------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `list_monitoring_actions`   | `acknowledgement` `downtime`                     | List current acknowledgements or downtimes, with pagination and sorting.                                           |
| `set_monitoring_actions`    | `acknowledgement` `downtime` `comment` `check` | Acknowledge, schedule a downtime, attach a comment, or trigger a check without waiting for the next polling cycle. |
| `cancel_monitoring_actions` | `acknowledgement` `downtime`                     | Cancel one or more acknowledgements or downtimes by their IDs.                                                     |

Each tool accepts a `model_type` parameter to select the action kind. Acknowledge alerts, schedule downtimes, leave comments, and trigger checks without ever leaving your conversation.

### Metrics

| Tool                  | Types     | Description                                                                                          |
| --------------------- | --------- | ---------------------------------------------------------------------------------------------------- |
| `get_service_metrics` | `service` | Retrieve all metrics of a service with their current values, units, and warning/critical thresholds. |

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
