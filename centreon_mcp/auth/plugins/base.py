from abc import ABC, abstractmethod

from fastmcp import FastMCP
from fastmcp.server.auth import AccessToken, AuthProvider

from centreon_mcp.auth.models import Role, Tenant


class AuthPlugin(ABC):
    """
    Contract implemented by authentication plugins.
    """

    @abstractmethod
    def provider(self) -> AuthProvider | None:
        """
        Return the FastMCP authentication provider, or None for an unauthenticated server.
        """
        ...

    @abstractmethod
    async def tenant(self) -> Tenant:
        """
        Return the Centreon to call for the current request.

        Resolving a tenant may reach the network, for instance to mint a short lived Centreon
        token for the current user, hence the coroutine.
        """
        ...

    @abstractmethod
    async def role(self, token: AccessToken | None) -> Role:
        """
        Return the permission level of the authenticated user, NONE when it is granted none.

        Raise `AuthenticationError` to refuse this identity outright, which denies every tool and
        is logged as a decision. Any other exception is reported as a fault to investigate, and
        denies too, since a level that cannot be established must never grant.

        Called once per tool for every tool listing, so a plugin resolving the level over the
        network caches it itself: the core cannot choose how long that answer stays valid.
        """
        ...

    @abstractmethod
    async def tenants(self) -> list[Tenant]:
        """
        Return the tenants known upfront, used by the startup connectivity check.
        """
        ...

    def components(self) -> list[FastMCP]:
        """
        Return the tools this plugin adds to the server, mounted alongside the built-in ones.

        A plugin whose deployment needs a choice the generic tools know nothing about exposes it
        here rather than adding an argument to every tool. These tools declare their own level,
        and nothing in this package checks that they do.
        """
        return []
