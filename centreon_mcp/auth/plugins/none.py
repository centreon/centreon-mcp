from fastmcp.server.auth import AccessToken, AuthProvider
from fastmcp.server.dependencies import get_http_headers
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from centreon_mcp.auth.models import Role, Tenant
from centreon_mcp.auth.plugins.base import AuthPlugin


class NoAuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_ignore_empty=True, env_prefix="centreon_")

    base_url: str = Field(
        description="Base URL of the Centreon instance to connect to, e.g. `https://centreon.example.com`."
    )
    api_token: SecretStr | None = Field(
        default=None,
        description="Fallback Centreon API token, used when the MCP client does not supply one "
        "through the `centreon-api-token` header.",
    )


class NoAuthPlugin(AuthPlugin):
    """
    Authentication plugin exposing a single Centreon to unauthenticated clients.
    """

    def __init__(self) -> None:
        """
        Load the Centreon connection settings from the `CENTREON_*` environment variables.

        Fails at startup with a validation error when `CENTREON_BASE_URL` is missing.
        """
        self.settings = NoAuthSettings()  # type: ignore[call-arg]

    def provider(self) -> AuthProvider | None:
        """
        Leave the MCP server unauthenticated.
        """
        return None

    async def tenant(self) -> Tenant:
        """
        Build the configured Centreon from settings.

        The token carried by the `centreon-api-token` header takes precedence over the one set
        with `CENTREON_API_TOKEN`, so a client may act with its own Centreon rights.
        """
        header_api_token = get_http_headers().get("centreon-api-token")
        api_token = SecretStr(header_api_token) if header_api_token else None
        api_token = api_token or self.settings.api_token
        return Tenant(name="centreon", base_url=self.settings.base_url, api_token=api_token)

    async def role(self, token: AccessToken | None) -> Role:
        """
        Grant every tool, since the Centreon API token already carries the user rights.
        """
        return Role.ADMIN

    async def tenants(self) -> list[Tenant]:
        return [await self.tenant()]
