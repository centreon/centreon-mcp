from centreon_mcp.auth.base import Role
from centreon_mcp.auth.none import NoAuthPlugin

MODULE = "centreon_mcp.auth.none"


async def test_auth_provider():

    # Call test function: the server stays open, as it was before plugins existed
    assert NoAuthPlugin().auth_provider() is None


async def test_role():

    # Call test function: every tool is granted, the Centreon token carries the rights
    assert await NoAuthPlugin().role(None) == Role.ADMIN


async def test_components():

    # Call test function: this plugin adds no tool of its own
    assert NoAuthPlugin().components() == []
