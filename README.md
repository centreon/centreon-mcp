# Centreon MCP Server

This project offers an MCP server for Centreon. Built in Python with the [FastMCP](https://gofastmcp.com/getting-started/welcome) library, it enables users to perform operations on a Centreon instance using natural language commands.

## Features

Using natural language, you can ask the Centreon MCP server to:

### Keep an eye on your infrastructure

- Check the real-time status of your hosts and services, filtering by state, group, category, poller, and more.
- Get an instant count of how many resources are up, down, or in trouble, without digging through dashboards.
- Look back at what happened on a host or service recently — outages, notifications, downtimes, acknowledgements, and comments.

### Manage your monitoring configuration

- Browse, create, update, and delete hosts, services, and their categories, groups, severities, and templates.
- Manage commands, time periods and monitoring servers (pollers).
- Push configuration changes to your pollers by generating or reloading them on demand.

### React to incidents

- Acknowledge an alert, schedule a downtime, add a comment, or trigger an immediate check.
- Review current acknowledgements and downtimes, and cancel them when they're no longer needed.

### Analyze performance

- Retrieve a service's metrics along with their current values and warning/critical thresholds.

### Control access with pluggable authentication

- Choose how MCP clients authenticate and which Centreon instance each request targets by selecting an authentication plugin.
- Restrict tools by role: readers can list and inspect, editors can create, update and act on alerts, admins can also delete and push configuration to pollers.

> For the exact list of underlying tools, see [TOOLS.md](TOOLS.md).

## Quick Start

1. Clone the repository

```shell
git clone https://github.com/centreon/centreon-mcp.git
cd centreon-mcp
```

2. Set up authentication by choosing a plugin and setting its environment variables, as described in the [Authentication](#authentication) section.

3. Ensure all required environment variables are set. Default values are used for optional variables.

| Name                       | Required | Default     | Description                                                            |
| -------------------------- | -------- | ----------- | ---------------------------------------------------------------------- |
| `CENTREON_AUTH_PLUGIN`     | `False`  | `none`      | Authentication plugin to load, see [Authentication](#authentication).  |
| `CENTREON_CLIENT_TIMEOUT`  | `False`  | `30`        | Timeout, in seconds, for requests to the Centreon API.                 |
| `CENTREON_TLS_SECURE`      | `False`  | `True`      | Whether to verify the Centreon server's TLS certificate.               |
| `CENTREON_CA_BUNDLE`       | `False`  | `None`      | Path to a custom CA bundle used to verify the TLS certificate.         |
| `CENTREON_MCP_HOST`        | `False`  | `localhost` | Network interface the MCP HTTP server binds to.                        |
| `CENTREON_MCP_PORT`        | `False`  | `8000`      | TCP port the MCP HTTP server listens on.                               |
| `CENTREON_MCP_LOG_LEVEL`   | `False`  | `INFO`      | Lowest severity level emitted by the MCP service logs.                 |
| `CENTREON_MCP_WEBSITE_URL` | `False`  | `None`      | Website with more information about your server, shown in client apps. |

> Setting `CENTREON_TLS_SECURE` to `False` disables TLS certificate verification and is not recommended in production.

> If `CENTREON_CA_BUNDLE` is `None`, the system default CA store is used to verify the TLS certificate. 
> If `CENTREON_CA_BUNDLE` is set while TLS verification is enabled but the path does not exist, the server refuses to start.

> Available log level for Centreon service are: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

### Using UV

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

4. Build Docker image

```shell
docker build -t centreon/mcp .
```

5. Start the MCP server

```shell
docker compose up
```

6. To make it reachable from the internet, export `NGROK_AUTHTOKEN` in the environment and enable `ngrok` profile.

```shell
docker compose --profile ngrok up
```

> Use `curl http://localhost:4040/api/tunnels` to retrieve public URL

## Authentication

Authentication is handled by a plugin, selected with the `CENTREON_AUTH_PLUGIN` environment variable. The plugin decides:

- how MCP clients authenticate to the MCP server;
- which Centreon instance, and with which API token, each request targets;
- which role the user is granted, and therefore which tools they can call.

| Role     | Granted tools                                                                         |
| -------- | ------------------------------------------------------------------------------------- |
| `READER` | List, get and count tools.                                                            |
| `EDITOR` | `READER` tools, plus create/update tools and setting or cancelling monitoring actions. |
| `ADMIN`  | `EDITOR` tools, plus delete tools and poller generate/reload.                         |

Each plugin reads its own settings from `CENTREON_*` environment variables, described in its section below.

### `none` (default)

Leaves the MCP server unauthenticated and serves a single Centreon instance. Every client is granted the `ADMIN` role: what a client can actually do is bounded by the rights of the Centreon API token in use.

| Name                 | Required | Default | Description                                              |
| -------------------- | -------- | ------- | -------------------------------------------------------- |
| `CENTREON_BASE_URL`  | `True`   |         | Base URL of the Centreon instance to connect to.         |
| `CENTREON_API_TOKEN` | `False`  | `None`  | Fallback API token, used when the MCP client sends none. |

> The server refuses to start if `CENTREON_BASE_URL` is not set.

> A token sent by the MCP client in the `centreon-api-token` header takes precedence over `CENTREON_API_TOKEN`, so each client can act with its own Centreon rights.

> Only use this plugin when the MCP server is not exposed to untrusted clients, or when every client provides its own Centreon API token.

## Integration

<details>
<summary>ChatGPT</summary>

1. Open [ChatGPT](https://chatgpt.com) and sign in.
2. Click on your profile picture in the bottom-left corner, then select **Settings**.
3. Go to the **Connectors** section and click **Create**.
4. Fill in the form:
   - **Name**: `Centreon` (or any name you prefer)
   - **URL**: the address of your running MCP server, e.g. `https://<ngrok-subdomain>.ngrok-free.app/mcp`
   - **Headers**: Optionally, provide a valid Centreon API token in the `centreon-api-token` header. This token takes precedence over the token specified through the `CENTREON_API_TOKEN` environment variable.
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
   - **Headers**: Optionally, provide a valid Centreon API token in the `centreon-api-token` header. This token takes precedence over the token specified through the `CENTREON_API_TOKEN` environment variable.
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

> Don't set `-H "centreon-api-token: <token>"` to use token specified through the `CENTREON_API_TOKEN` environment variable instead.

List configured MCP servers and confirm `centreon` is present:

```shell
/mcp list
```

</details>
