"""
Pluggable authentication and role based authorization.

Who the caller is and what they may do is answered by the `AuthPlugin` contract of `base.py`.
`CENTREON_AUTH_PLUGIN` selects one, by built-in name, by `centreon_mcp.auth` entry point, or by
`module:attribute` path.
"""

from importlib import import_module
from importlib.metadata import entry_points

from fastmcp.exceptions import AuthorizationError
from fastmcp.server.auth import AuthCheck, AuthContext

from centreon_mcp import logger, settings
from centreon_mcp.auth.base import AuthenticationError, AuthPlugin, Role

ENTRY_POINT_GROUP = "centreon_mcp.auth"

BUILT_IN_PLUGINS = {
    "none": "centreon_mcp.auth.none:NoAuthPlugin",
    "oidc": "centreon_mcp.auth.oidc:OIDCPlugin",
}

AUTH_PLUGIN_METHODS = ("auth_provider", "role", "components")


def import_plugin(path: str) -> AuthPlugin:
    """
    Instantiate the plugin class designated by a `module:attribute` import path.
    """
    module_name, _, attribute = path.partition(":")
    return getattr(import_module(module_name), attribute)()


def load_plugin(name: str) -> AuthPlugin:
    """
    Load an authentication plugin by built-in name, entry point name, or import path.

    Built-in names win over entry points, so a package cannot publish one under a reserved name.
    """
    try:
        plugin = resolve_plugin(name)
    except (ImportError, AttributeError) as error:
        raise ValueError(f"CENTREON_AUTH_PLUGIN '{name}' could not be loaded: {error}") from error

    # The protocol is the whole contract a separate package implements, so a plugin missing a
    # method is caught here rather than as an AttributeError on someone's first request
    if not isinstance(plugin, AuthPlugin):
        missing = [m for m in AUTH_PLUGIN_METHODS if not callable(getattr(plugin, m, None))]
        raise TypeError(
            f"CENTREON_AUTH_PLUGIN '{name}' does not implement AuthPlugin, "
            f"missing: {', '.join(missing) or 'unknown'}"
        )
    return plugin


def resolve_plugin(name: str) -> AuthPlugin:
    """
    Instantiate the plugin the given name designates, whichever way it is published.
    """
    if name in BUILT_IN_PLUGINS:
        logger.debug(f"Loading built-in authentication plugin {name}")
        return import_plugin(BUILT_IN_PLUGINS[name])

    for entry_point in entry_points(group=ENTRY_POINT_GROUP):
        if entry_point.name == name:
            logger.debug(f"Loading authentication plugin {name} from entry point")
            return entry_point.load()()

    if ":" in name:
        logger.debug(f"Loading authentication plugin from import path {name}")
        return import_plugin(name)

    available = sorted(
        {*BUILT_IN_PLUGINS, *(e.name for e in entry_points(group=ENTRY_POINT_GROUP))}
    )
    raise ValueError(
        f"Unknown authentication plugin '{name}'. "
        f"Available plugins: {', '.join(available)}. "
        "A 'module:attribute' import path is also accepted."
    )


# The plugin is loaded on first use rather than at import time: a plugin that calls Centreon
# imports `utils.request`, which needs this module, and loading eagerly would close that cycle
# while this very module is still initialising.
plugin: AuthPlugin | None = None


def get_plugin() -> AuthPlugin:
    """
    Return the configured authentication plugin, loading it once on first use.
    """
    global plugin

    if plugin is None:
        plugin = load_plugin(settings.auth_plugin)
    return plugin


def require_role(level: Role) -> AuthCheck:
    """
    Build the authorization check granting a tool to users of at least the given level.

    Tools whose check does not pass are hidden from tool listings and cannot be called.
    """

    async def check(context: AuthContext) -> bool:
        # An unauthenticated server grants every tool: access is already restricted by the
        # Centreon API token the server calls Centreon with
        if get_plugin().auth_provider() is None:
            return True

        if context.token is None:
            logger.debug(f"Denying {context.component.name}: request is not authenticated")
            return False

        # Requiring no level means being authenticated is the whole requirement. Asking the
        # plugin anyway would hide these tools from the very users they exist to inform, since
        # resolving a level is exactly what fails for a user the deployment grants nothing
        if level is Role.NONE:
            return True

        try:
            role = await get_plugin().role(context.token)
        except AuthorizationError:
            # FastMCP propagates this one on purpose, to answer the caller rather than hide the
            # tool. Catching it below would turn a plugin's deliberate refusal into a reported bug
            raise
        except AuthenticationError as error:
            # The plugin refused this identity on purpose. Worth a line, since the caller only
            # sees a tool that is not there, but not a fault to investigate
            logger.info(f"Denying {context.component.name}: {error}")
            return False
        except Exception as error:  # noqa: BLE001 — any plugin failure must deny, never grant
            # A denial and a fault both end as a hidden tool, so the distinction only survives
            # here: a plugin that cannot answer is something to investigate
            logger.error(
                f"Cannot resolve the role for {context.component.name}: {error}", exc_info=True
            )
            return False

        granted = role >= level
        if not granted:
            # Debug, not info: hiding a tool above the caller level is how a listing is meant to
            # work, and this runs for every tool of every listing
            logger.debug(
                f"Denying {context.component.name}: role {role.name} is below {level.name}"
            )
        return granted

    return check


AUTHENTICATED = require_role(Role.NONE)
READER = require_role(Role.READER)
EDITOR = require_role(Role.EDITOR)
ADMIN = require_role(Role.ADMIN)

__all__ = [
    "ADMIN",
    "AUTHENTICATED",
    "BUILT_IN_PLUGINS",
    "EDITOR",
    "ENTRY_POINT_GROUP",
    "READER",
    "AuthPlugin",
    "AuthenticationError",
    "Role",
    "get_plugin",
    "load_plugin",
    "require_role",
]
