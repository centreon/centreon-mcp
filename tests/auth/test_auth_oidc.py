from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from centreon_mcp import settings
from centreon_mcp.auth.base import AuthenticationError, Role, Tenant
from centreon_mcp.auth.oidc import OIDCPlugin, OIDCSettings, claim

MODULE = "centreon_mcp.auth.oidc"

CONFIG_URL = "https://idp.example.com/.well-known/openid-configuration"


def build(**overrides) -> OIDCPlugin:
    """
    Build a plugin with the given configuration, bypassing the environment.
    """
    plugin = OIDCPlugin.__new__(OIDCPlugin)
    plugin.settings = OIDCSettings(
        config_url=CONFIG_URL,
        client_id="client-id",
        client_secret="client-secret",
        **overrides,
    )
    plugin.provider = None
    plugin.reported = set()
    return plugin


def token(claims: dict) -> MagicMock:
    """
    Build an access token carrying the given claims.
    """
    access_token = MagicMock()
    access_token.claims = claims
    return access_token


@pytest.mark.parametrize(
    "claims,path,values",
    [
        ({"roles": ["editor", "reader"]}, "roles", ["editor", "reader"]),
        ({"scope": "openid profile"}, "scope", ["openid", "profile"]),
        ({"org_id": "org_1"}, "org_id", ["org_1"]),
        ({"realm_access": {"roles": ["admin"]}}, "realm_access.roles", ["admin"]),
        ({"count": 3}, "count", ["3"]),
        ({"roles": None}, "roles", []),
        ({}, "roles", []),
        ({"realm_access": "flat"}, "realm_access.roles", []),
    ],
)
async def test_claim(claims: dict, path: str, values: list[str]):

    # Call test function
    assert claim(claims, path) == values


@patch(f"{MODULE}.OIDCProxy", new_callable=MagicMock)
async def test_auth_provider(oidc_proxy: MagicMock):

    # Setup args
    plugin = build(audience="https://api.example.com", jwt_signing_key="signing-key")

    # Call test function
    with patch.object(settings, "mcp_public_url", "https://mcp.example.com"):
        provider = plugin.auth_provider()

    # Assert the provider was built with the configured identity provider
    oidc_proxy.assert_called_once_with(
        config_url=CONFIG_URL,
        client_id="client-id",
        client_secret="client-secret",
        audience="https://api.example.com",
        base_url="https://mcp.example.com",
        required_scopes=["openid", "profile", "email"],
        jwt_signing_key="signing-key",
    )
    assert provider == oidc_proxy.return_value

    # Assert the provider is built once and reused across requests
    with patch.object(settings, "mcp_public_url", "https://mcp.example.com"):
        assert plugin.auth_provider() == provider
    oidc_proxy.assert_called_once()


@patch(f"{MODULE}.OIDCProxy", new_callable=MagicMock)
async def test_auth_provider_without_public_url(oidc_proxy: MagicMock):

    # Setup args
    plugin = build()

    # Call test function
    with (
        patch.object(settings, "mcp_public_url", None),
        pytest.raises(AuthenticationError, match="CENTREON_MCP_PUBLIC_URL is required"),
    ):
        _ = plugin.auth_provider()


async def test_tenant_single():

    # Setup args: no tenant claim means a single Centreon serves every user
    plugin = build()

    # Call test function
    tenant = await plugin.tenant(token({}))

    # Assert the configured Centreon is returned
    assert tenant.base_url == settings.base_url
    assert tenant.token == settings.api_token


async def test_tenant_single_without_base_url():

    # Setup args
    plugin = build()

    # Call test function
    with (
        patch.object(settings, "base_url", None),
        pytest.raises(AuthenticationError, match="CENTREON_BASE_URL is required"),
    ):
        _ = await plugin.tenant(token({}))


async def test_tenant_by_claim():

    # Setup args
    customer = Tenant(name="customer", base_url="http://customer.example.com", api_token="token")
    plugin = build(tenant_claim="org_id", tenants={"org_1": customer})

    # Call test function
    assert await plugin.tenant(token({"org_id": "org_1"})) == customer


async def test_tenant_unknown():

    # Setup args
    plugin = build(tenant_claim="org_id", tenants={})

    # Call test function
    with pytest.raises(AuthenticationError, match="No Centreon is registered for org_id org_1"):
        _ = await plugin.tenant(token({"org_id": "org_1"}))


async def test_tenant_missing_claim():

    # Setup args
    plugin = build(tenant_claim="org_id", tenants={})

    # Call test function
    with pytest.raises(AuthenticationError, match="org_id <missing>"):
        _ = await plugin.tenant(token({}))


async def test_tenant_without_token():

    # Setup args
    plugin = build(tenant_claim="org_id", tenants={})

    # Call test function
    with pytest.raises(AuthenticationError, match="not authenticated"):
        _ = await plugin.tenant(None)


@pytest.mark.parametrize(
    "claims,role",
    [
        ({"roles": ["centreon-reader"]}, Role.READER),
        ({"roles": ["centreon-editor"]}, Role.EDITOR),
        ({"roles": ["centreon-admin"]}, Role.ADMIN),
        # The most privileged of the granted roles wins
        ({"roles": ["centreon-reader", "centreon-admin"]}, Role.ADMIN),
        # Roles that are not mapped are ignored
        ({"roles": ["unrelated", "centreon-editor"]}, Role.EDITOR),
    ],
)
async def test_role(claims: dict, role: Role):

    # Setup args
    plugin = build(
        role_mapping={
            "centreon-reader": "reader",
            "centreon-editor": "editor",
            "centreon-admin": "admin",
        }
    )

    # Call test function
    assert await plugin.role(token(claims)) == role


async def test_role_nested_claim():

    # Setup args: Keycloak nests realm roles
    plugin = build(role_claim="realm_access.roles", role_mapping={"ops": "editor"})

    # Call test function
    assert await plugin.role(token({"realm_access": {"roles": ["ops"]}})) == Role.EDITOR


async def test_role_default():

    # Setup args
    plugin = build(role_mapping={"ops": "admin"}, default_role="reader")

    # Call test function: an unmapped user falls back to the configured default
    assert await plugin.role(token({"roles": ["unrelated"]})) == Role.READER


@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_role_denied(logger: MagicMock):

    # Setup args
    plugin = build(role_mapping={"ops": "admin"})

    # Call test function: without a default role, an unmapped user is granted nothing
    assert await plugin.role(token({"roles": ["unrelated"]})) == Role.NONE

    # Assert the claim values were reported, so a wrong claim path can be told from a denied user
    assert "unrelated" in logger.warning.call_args.args[0]


@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_role_missing_claim(logger: MagicMock):

    # Setup args
    plugin = build(role_claim="realm_access.roles", role_mapping={"ops": "admin"})

    # Call test function: a claim path matching nothing is reported, not silently treated as empty
    assert await plugin.role(token({"roles": ["ops"]})) == Role.NONE

    # Assert the log says the claim carried nothing rather than naming a value
    assert "nothing" in logger.warning.call_args.args[0]


async def test_role_without_token():

    # Setup args
    plugin = build()

    # Call test function
    with pytest.raises(AuthenticationError, match="not authenticated"):
        _ = await plugin.role(None)


@pytest.mark.parametrize(
    "overrides",
    [
        {"role_mapping": {"ops": "superuser"}},
        {"default_role": "superuser"},
    ],
)
async def test_unknown_role_configured(overrides: dict):

    # Call test function: a typo fails at startup rather than on the first request
    with pytest.raises(ValidationError, match="Unknown role"):
        _ = build(**overrides)


async def test_tenants():

    # Setup args
    customer = Tenant(name="customer", base_url="http://customer.example.com", api_token="token")
    plugin = build(tenant_claim="org_id", tenants={"org_1": customer})

    # Call test function
    assert plugin.tenants() == [customer]


async def test_tenants_single():

    # Setup args
    plugin = build()

    # Call test function
    assert [tenant.base_url for tenant in plugin.tenants()] == [settings.base_url]


async def test_tenants_single_without_base_url():

    # Setup args
    plugin = build()

    # Call test function: nothing can be checked at startup
    with patch.object(settings, "base_url", None):
        assert plugin.tenants() == []


async def test_settings_from_environment(monkeypatch: pytest.MonkeyPatch):

    # Mock the environment of a deployment serving several Centreon
    monkeypatch.setenv("CENTREON_OIDC_CONFIG_URL", CONFIG_URL)
    monkeypatch.setenv("CENTREON_OIDC_CLIENT_ID", "client-id")
    monkeypatch.setenv("CENTREON_OIDC_CLIENT_SECRET", "client-secret")
    monkeypatch.setenv("CENTREON_OIDC_ROLE_CLAIM", "realm_access.roles")
    monkeypatch.setenv("CENTREON_OIDC_ROLE_MAPPING", '{"ops": "admin"}')
    monkeypatch.setenv("CENTREON_OIDC_TENANT_CLAIM", "org_id")
    monkeypatch.setenv(
        "CENTREON_OIDC_TENANTS",
        '{"org_1": {"name": "customer", "base_url": "http://customer.example.com",'
        ' "api_token": "token"}}',
    )

    # Call test function
    plugin = OIDCPlugin()

    # Assert the configuration was read from the environment
    assert plugin.settings.role_claim == "realm_access.roles"
    assert plugin.settings.client_secret.get_secret_value() == "client-secret"
    assert await plugin.role(token({"realm_access": {"roles": ["ops"]}})) == Role.ADMIN
    assert (await plugin.tenant(token({"org_id": "org_1"}))).token == "token"


@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_role_reports_an_unmapped_claim_once(logger: MagicMock):

    # Setup args
    plugin = build(role_mapping={"ops": "admin"})

    # Call test function: the level is resolved for every tool of every listing
    for _ in range(3):
        _ = await plugin.role(token({"roles": ["unrelated"]}))
    _ = await plugin.role(token({"roles": ["other"]}))

    # Assert a misconfiguration is reported without drowning the log
    assert logger.warning.call_count == 2
