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

> For the exact list of underlying tools, see [TOOLS.md](TOOLS.md).

## Quick Start

1. Clone the repository

```shell
git clone https://github.com/centreon/centreon-mcp.git
cd centreon-mcp
```

2. Ensure all required environment variables are set. Default values are used for optional variables.

| Name                       | Required | Default     | Description                                                         |
| -------------------------- | -------- | ----------- | ------------------------------------------------------------------- |
| `CENTREON_BASE_URL`        | Depends  |             | Base URL of the Centreon instance.                                  |
| `CENTREON_API_TOKEN`       | `False`  | `None`      | Centreon API token used if not provided through MCP client headers. |
| `CENTREON_CLIENT_TIMEOUT`  | `False`  | `30`        | Timeout for Centreon API client.                                    |
| `CENTREON_MCP_HOST`        | `False`  | `localhost` | Host used to start the Centreon MCP service.                        |
| `CENTREON_MCP_PORT`        | `False`  | `8000`      | Port used to start the Centreon MCP service.                        |
| `CENTREON_MCP_LOG_LEVEL`   | `False`  | `INFO`      | Minimal severity level for Centreon MCP service logs.               |
| `CENTREON_MCP_PUBLIC_URL`  | `False`  | `None`      | Public URL of the MCP server, required to authenticate users.       |
| `CENTREON_AUTH_PLUGIN`     | `False`  | `none`      | Authentication plugin used to identify users.                       |
| `CENTREON_MCP_ICON_URL`    | `False`  | `None`      | Logo shown on the consent screen users see before signing in.       |
| `CENTREON_MCP_WEBSITE_URL` | `False`  | `None`      | Link behind the server name on that screen.                         |

> Available log level for Centreon service are: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

> `CENTREON_BASE_URL` is required by the default `none` plugin. See [Authentication](#authentication)
> for deployments serving several Centreon instances.

### Using UV

3. Start the MCP server

```shell
uv run centreon-mcp-server
```

4. If the MCP server is not reachable from the internet, expose it using a tunneling tool such as [Ngrok](https://ngrok.com):

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

## Authentication

By default the MCP server does not authenticate its users: it exposes every tool and calls Centreon
with the token sent in the `centreon-api-token` header, falling back to `CENTREON_API_TOKEN`. Rights
are those of that token in Centreon. This is the `none` plugin, and it is what most on premise
deployments need.

Deployments that want their users to sign in, or that serve several Centreon instances from a single
MCP server, select another plugin with `CENTREON_AUTH_PLUGIN`. A plugin answers three questions:
how users authenticate, which Centreon a given user reaches, and what that user is allowed to do.

### Permission levels

Tools are gated by three cumulative levels. Tools above the level of the current user are hidden from
the tool list and cannot be called, so a client never offers an action its user may not perform.

| Level    | Grants                                                                                                                         |
| -------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `reader` | Read monitoring status, configuration, timelines and metrics.                                                                  |
| `editor` | Everything a reader may do, plus create and update configuration, acknowledge, schedule downtimes, comment and trigger checks. |
| `admin`  | Everything an editor may do, plus delete configuration and generate or reload pollers.                                         |

A user the deployment grants no level to reaches no tool at all, except `get_current_context`,
which requires none: it reports the Centreon and the level in effect, so such a user is told why
every other tool is missing rather than facing a server that appears to expose none.

The level required by each tool is listed in [TOOLS.md](TOOLS.md).

### The `oidc` plugin

Authenticates users against any OpenID Connect provider (Keycloak, Entra, Auth0, Okta, ...). Register
the MCP server as a confidential client of your provider, with `{CENTREON_MCP_PUBLIC_URL}/auth/callback`
as its redirect URI. MCP clients then sign in through your provider instead of carrying a Centreon
token themselves, and the `centreon-api-token` header is ignored.

| Name                            | Required | Default                | Description                                                                                               |
| ------------------------------- | -------- | ---------------------- | --------------------------------------------------------------------------------------------------------- |
| `CENTREON_OIDC_CONFIG_URL`      | `True`   |                        | OpenID Connect discovery URL of the provider.                                                             |
| `CENTREON_OIDC_CLIENT_ID`       | `True`   |                        | Client ID registered for the MCP server.                                                                  |
| `CENTREON_OIDC_CLIENT_SECRET`   | `True`   |                        | Client secret registered for the MCP server.                                                              |
| `CENTREON_OIDC_AUDIENCE`        | `False`  | `None`                 | API audience. Set it: left unset, tokens are accepted whatever audience they were issued for.             |
| `CENTREON_OIDC_SCOPES`          | `False`  | `openid profile email` | Scopes requested at login.                                                                                |
| `CENTREON_OIDC_JWT_SIGNING_KEY` | `False`  | `None`                 | Signing key of the tokens issued to MCP clients. Required when several workers serve the same deployment. |
| `CENTREON_OIDC_ROLE_CLAIM`      | `False`  | `roles`                | Claim holding the roles of the user, as a dotted path.                                                    |
| `CENTREON_OIDC_ROLE_MAPPING`    | `False`  | `{}`                   | JSON mapping claim values to `reader`, `editor` or `admin`.                                               |
| `CENTREON_OIDC_DEFAULT_ROLE`    | `False`  | `None`                 | Level granted to users no mapping applies to. Without it, such users are granted no level.                |
| `CENTREON_OIDC_TENANT_CLAIM`    | `False`  | `None`                 | Claim selecting the Centreon to call. Unset means a single Centreon serves everyone.                      |
| `CENTREON_OIDC_TENANTS`         | `False`  | `{}`                   | JSON mapping tenant claim values to a Centreon and its API token.                                         |

A Keycloak deployment reading realm roles, serving one Centreon:

```shell
CENTREON_AUTH_PLUGIN=oidc
CENTREON_MCP_PUBLIC_URL=https://mcp.example.com
CENTREON_OIDC_CONFIG_URL=https://keycloak.example.com/realms/main/.well-known/openid-configuration
CENTREON_OIDC_CLIENT_ID=centreon-mcp
CENTREON_OIDC_CLIENT_SECRET=<secret>
CENTREON_OIDC_ROLE_CLAIM=realm_access.roles
CENTREON_OIDC_ROLE_MAPPING='{"centreon-admins": "admin", "centreon-ops": "editor", "centreon-users": "reader"}'
```

Serving several Centreon instances, one per tenant, adds the tenant claim and its table:

```shell
CENTREON_OIDC_TENANT_CLAIM=org_id
CENTREON_OIDC_TENANTS='{"org_1": {"name": "acme", "base_url": "https://acme.example.com/centreon", "api_token": "<token>"}}'
```

> Each Centreon is called with the service token configured for its tenant, not with credentials of
> the end user, so Centreon ACLs do not apply per user. Give that token the rights an `admin` may
> exercise, and rely on the permission levels above to restrict everyone else.

### Writing a plugin

Deployments whose identity model does not fit the `oidc` plugin ship their own, in a separate
package. A plugin implements the `AuthPlugin` protocol of `centreon_mcp.auth.base`:

```python
class AuthPlugin(Protocol):
    def auth_provider(self) -> AuthProvider | None: ...  # None leaves the server unauthenticated
    async def tenant(self, token: AccessToken | None) -> Tenant: ...  # may reach the network
    async def role(self, token: AccessToken | None) -> Role: ...  # called once per tool listed
    def tenants(self) -> Sequence[Tenant] | None: ...  # None: resolved per request, not checked
    def components(self) -> Sequence[FastMCP]: ...  # extra tools, mounted with the built-in ones
```

A plugin whose deployment needs a choice the generic tools know nothing about, such as which of
several platforms of a tenant to act on, exposes it through `components` rather than adding an
argument to every tool.

Publish it in the `centreon_mcp.auth` entry point group and select it by name:

```toml
[project.entry-points."centreon_mcp.auth"]
acme = "acme_mcp_auth.plugin:AcmePlugin"
```

`CENTREON_AUTH_PLUGIN` also accepts a `module:attribute` import path, which is convenient while
developing a plugin.

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
