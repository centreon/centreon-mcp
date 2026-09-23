"""
Unauthenticated plugin, the default, granting every tool to every caller.

The Centreon API token already carries the rights of whoever calls, so there is nothing for this
server to decide.
"""

from collections.abc import Sequence

from fastmcp import FastMCP
from fastmcp.server.auth import AccessToken
from fastmcp.server.auth.auth import AuthProvider

from centreon_mcp.auth.base import Role


class NoAuthPlugin:
    """
    Authentication plugin leaving the MCP server open, as it was before plugins existed.
    """

    def auth_provider(self) -> AuthProvider | None:
        """
        Leave the MCP server unauthenticated.
        """
        return None

    async def role(self, token: AccessToken | None = None) -> Role:
        """
        Grant every tool, since the Centreon API token already carries the user rights.
        """
        return Role.ADMIN

    def components(self) -> Sequence[FastMCP]:
        return []
