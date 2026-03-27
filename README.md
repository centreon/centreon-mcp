# Centreon MCP Server

This project offers an MCP server for Centreon. Built in Python with the [FastMCP](https://gofastmcp.com/getting-started/welcome) library, it enables users to perform operations on a Centreon instance using natural language commands.

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
uv run mcp
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
claude mcp list
```

</details>