"""
Unauthenticated plugin, preserving the historical single Centreon behaviour.

The token comes from the `centreon-api-token` header, falling back to `CENTREON_API_TOKEN`, and
every tool is granted since that token already carries the user rights in Centreon.
"""

from collections.abc import Sequence

from fastmcp import FastMCP
from fastmcp.server.auth import AccessToken
from fastmcp.server.auth.auth import AuthProvider
from fastmcp.server.dependencies import get_http_headers
from pydantic import SecretStr

from centreon_mcp import settings
from centreon_mcp.auth.base import AuthenticationError, Role, Tenant

TOKEN_HEADER = "centreon-api-token"

# Reported by get_current_context. The base URL would name it more precisely, but it is an
# internal address and the tool answer leaves the deployment
TENANT_NAME = "centreon"


class LegacyPlugin:
    """
    Authentication plugin exposing a single Centreon to unauthenticated clients.
    """

    def auth_provider(self) -> AuthProvider | None:
        """
        Leave the MCP server unauthenticated.
        """
        return None

    async def tenant(self, token: AccessToken | None = None) -> Tenant:
        return self.build_tenant()

    def build_tenant(self) -> Tenant:
        """
        Build the configured Centreon.

        The token carried by the `centreon-api-token` header takes precedence over the one set
        with `CENTREON_API_TOKEN`, so a client may act with its own Centreon rights.
        """
        if settings.base_url is None:
            raise AuthenticationError(
                "CENTREON_BASE_URL is required by the 'none' authentication plugin"
            )

        api_token = get_http_headers().get(TOKEN_HEADER) or settings.api_token
        return Tenant(
            name=TENANT_NAME,
            base_url=settings.base_url,
            api_token=SecretStr(api_token) if api_token else None,
        )

    async def role(self, token: AccessToken | None = None) -> Role:
        """
        Grant every tool, since the Centreon API token already carries the user rights.
        """
        return Role.ADMIN

    def tenants(self) -> Sequence[Tenant]:
        return [self.build_tenant()]

    def components(self) -> Sequence[FastMCP]:
        return []
