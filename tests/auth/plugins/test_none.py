from unittest.mock import MagicMock

import pytest

from centreon_mcp.auth.models import Role, Tenant
from centreon_mcp.auth.plugins.none import NoAuthPlugin


@pytest.fixture
def plugin() -> NoAuthPlugin:
    return NoAuthPlugin()


def test_provider(plugin: NoAuthPlugin):

    # Call test function
    provider = plugin.provider()

    # Assertions
    assert provider is None


async def test_tenant(plugin: NoAuthPlugin):

    # Call test function
    tenant = await plugin.tenant()

    # Assertions
    assert tenant == Tenant(
        name="centreon", base_url=plugin.settings.base_url, api_token=plugin.settings.api_token
    )


@pytest.mark.parametrize("token", [None, MagicMock()])
async def test_role(plugin: NoAuthPlugin, token: MagicMock | None):

    # Call test function
    role = await plugin.role(token)

    # Assertions
    assert role is Role.ADMIN


async def test_tenants(plugin: NoAuthPlugin):

    # Call test function
    tenants = await plugin.tenants()

    # Assertions
    assert tenants == [await plugin.tenant()]
