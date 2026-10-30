from fastmcp.server.auth import AccessToken, AuthProvider
from pydantic_settings import BaseSettings

from centreon_mcp.auth.models import Role, Tenant
from centreon_mcp.auth.plugins.base import AuthPlugin


class DummyPlugin(AuthPlugin[BaseSettings]):
    """
    Minimal plugin relying on every default the base class provides.
    """

    settings_cls = BaseSettings

    def provider(self) -> AuthProvider | None:
        return None

    async def tenant(self) -> Tenant:
        raise NotImplementedError

    async def role(self, token: AccessToken | None) -> Role:
        raise NotImplementedError

    async def tenants(self) -> list[Tenant]:
        return []


def test_components():

    plugin = DummyPlugin()

    # Call test function
    components = plugin.components()

    # Assertions
    assert components == []
