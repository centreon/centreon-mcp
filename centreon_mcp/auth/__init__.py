from collections.abc import Awaitable, Callable
from importlib.metadata import entry_points

from fastmcp.server.auth import AuthContext

from centreon_mcp import settings
from centreon_mcp.auth.models import Role
from centreon_mcp.auth.plugins.base import AuthPlugin

plugin: AuthPlugin

ENTRY_POINTS_GROUP = "centreon_mcp.auth"


def load() -> None:
    """
    Instantiate authentication plugin given by CENTREON_AUTH_PLUGIN environment variable.
    """
    global plugin

    name = settings.auth_plugin

    plugins = {
        entry_point.name: entry_point for entry_point in entry_points(group=ENTRY_POINTS_GROUP)
    }

    if name not in plugins:
        raise ValueError(
            f"Unknown authentication plugin '{name}'. Available plugins: {','.join(plugins)}. "
        )

    plugin = plugins[name].load()()


def require_roles(level: Role) -> Callable[[AuthContext], Awaitable[bool]]:
    """
    Build the authorization check granting a tool to users of at least the given level.
    """

    async def check(context: AuthContext) -> bool:

        # Get role of current user
        role = await plugin.role(context.token)

        # Grant tool if user role is higher or equal to level
        return role >= level

    return check
