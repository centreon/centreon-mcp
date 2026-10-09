"""
Generic OpenID Connect plugin.

Users authenticate against any OpenID Connect provider, and the permission level is read from a
claim of the access token. Providers name things differently, so the claim path and the value
mapping are configuration.
"""

from collections.abc import Sequence
from typing import Any

from fastmcp import FastMCP
from fastmcp.server.auth import AccessToken
from fastmcp.server.auth.auth import AuthProvider
from fastmcp.server.auth.oidc_proxy import OIDCProxy
from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from centreon_mcp import logger, settings
from centreon_mcp.auth.base import AuthenticationError, Role

# Role.NONE is what a user who matches nothing is left with, never something to map a claim to
ROLES = {role.name.lower(): role for role in Role if role is not Role.NONE}

# How many distinct claim values are remembered before starting to report them again
REPORT_LIMIT = 100


class OIDCSettings(BaseSettings):
    """
    Configuration of the generic OpenID Connect plugin.
    """

    model_config = SettingsConfigDict(env_ignore_empty=True, env_prefix="centreon_oidc_")

    config_url: str
    client_id: str
    client_secret: SecretStr
    audience: str | None = None
    scopes: str = "openid profile email"
    jwt_signing_key: SecretStr | None = None
    role_claim: str = "roles"
    role_mapping: dict[str, str] = {}
    default_role: str | None = None

    @field_validator("role_mapping", "default_role")
    @classmethod
    def check_roles(cls, value: dict[str, str] | str | None) -> dict[str, str] | str | None:
        """
        Reject unknown role names, so a typo fails at startup and not on the first request.
        """
        names = value.values() if isinstance(value, dict) else [value] if value else []
        unknown = sorted({name for name in names if name.lower() not in ROLES})
        if unknown:
            raise ValueError(
                f"Unknown role(s) {', '.join(unknown)}. Valid roles: {', '.join(ROLES)}"
            )
        return value


def claim(claims: dict[str, Any], path: str) -> list[str]:
    """
    Read a claim designated by a dotted path and return its values as a list of strings.

    Providers expose claims as a single value (`org_id`), a list (`roles`), or a space
    separated string (`scope`), and nest them at arbitrary depths (`realm_access.roles`).

    A single value is split on whitespace, so a claim value must not contain spaces.
    """
    value: Any = claims
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return []
        value = value[part]

    if isinstance(value, str):
        return value.split()
    if isinstance(value, (list, tuple)):
        return [str(item) for item in value]
    if value is None:
        return []
    return [str(value)]


class OIDCPlugin:
    """
    Authentication plugin bridging the MCP server to an OpenID Connect provider.
    """

    def __init__(self) -> None:
        self.settings = OIDCSettings()  # type: ignore[call-arg]
        self.provider: AuthProvider | None = None
        self.reported: set[tuple[str, ...]] = set()

    def auth_provider(self) -> AuthProvider | None:
        """
        Return the OpenID Connect provider, built once and reused across requests.
        """
        if self.provider is None:
            if settings.mcp_public_url is None:
                raise AuthenticationError(
                    "CENTREON_MCP_PUBLIC_URL is required by the 'oidc' authentication plugin"
                )

            signing_key = self.settings.jwt_signing_key
            self.provider = OIDCProxy(
                config_url=self.settings.config_url,
                client_id=self.settings.client_id,
                client_secret=self.settings.client_secret.get_secret_value(),
                audience=self.settings.audience,
                base_url=settings.mcp_public_url,
                required_scopes=self.settings.scopes.split(),
                jwt_signing_key=signing_key.get_secret_value() if signing_key else None,
            )
        return self.provider

    async def role(self, token: AccessToken | None) -> Role:
        """
        Return the highest permission level granted by the role claim of the access token.
        """
        if token is None:
            raise AuthenticationError("Request is not authenticated")

        values = claim(token.claims, self.settings.role_claim)
        granted = [
            ROLES[self.settings.role_mapping[value].lower()]
            for value in values
            if value in self.settings.role_mapping
        ]
        if granted:
            return max(granted)

        # A claim path that never matches is indistinguishable from a user granted nothing, and
        # silently hands everyone the default role, so say which of the two happened. Reported
        # once per set of values, since this runs for every tool of every listing
        # Capped: the keys come from token claims, so an unbounded set would grow with whatever
        # a provider puts there
        seen = tuple(values)
        if seen not in self.reported:
            if len(self.reported) >= REPORT_LIMIT:
                self.reported.clear()
            self.reported.add(seen)
            logger.warning(
                f"Claim {self.settings.role_claim} carried {', '.join(values) or 'nothing'}, "
                "which CENTREON_OIDC_ROLE_MAPPING maps to no role"
            )
        return (
            ROLES[self.settings.default_role.lower()] if self.settings.default_role else Role.NONE
        )

    def components(self) -> Sequence[FastMCP]:
        return []
