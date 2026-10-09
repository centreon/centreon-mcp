"""
Core types of the authentication layer, kept out of the package entry point, which plugins cannot
import while it is loading them.
"""

from collections.abc import Sequence
from enum import IntEnum
from typing import Protocol, runtime_checkable

from fastmcp import FastMCP
from fastmcp.server.auth import AccessToken
from fastmcp.server.auth.auth import AuthProvider


class AuthenticationError(Exception):
    """
    Raised when a request cannot be resolved to a permission level, including when the plugin
    that resolves it is misconfigured.
    """


class Role(IntEnum):
    """
    Permission levels, ordered from the least to the most privileged.

    A user is granted a tool when its own level is greater than or equal to the level required
    by that tool, so levels are cumulative: an editor may do everything a reader may do.

    NONE is the level of an authenticated user the deployment grants nothing to. It reaches the
    tools requiring no level, which is how such a user can be told why every other tool is
    missing, rather than facing a server that appears to expose none.
    """

    NONE = 0
    READER = 1
    EDITOR = 2
    ADMIN = 3


@runtime_checkable
class AuthPlugin(Protocol):
    """
    Contract implemented by authentication plugins.
    """

    def auth_provider(self) -> AuthProvider | None:
        """
        Return the FastMCP authentication provider, or None for an unauthenticated server.
        """
        ...

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

    def components(self) -> Sequence[FastMCP]:
        """
        Return the tools this plugin adds to the server, mounted alongside the built-in ones.

        A plugin whose deployment needs a choice the generic tools know nothing about exposes it
        here rather than adding an argument to every tool. These tools declare their own level,
        and nothing in this package checks that they do.
        """
        ...
