from enum import IntEnum

from pydantic import BaseModel, SecretStr


class AuthenticationError(Exception):
    """
    Raised when a request cannot be resolved to a tenant or a permission level, including when
    the plugin that resolves it is misconfigured.
    """


class Role(IntEnum):
    """
    Permission levels, ordered from the least to the most privileged.

    A user is granted a tool when its own level is greater than or equal to the level required
    by that tool, so levels are cumulative: an editor may do everything a reader may do.
    """

    NONE = 0
    READER = 1
    EDITOR = 2
    ADMIN = 3


class Tenant(BaseModel):
    """
    A Centreon reachable by the MCP server, with the credentials used to call it.
    """

    name: str
    base_url: str
    api_token: SecretStr | None = None

    @property
    def token(self) -> str | None:
        return self.api_token.get_secret_value() if self.api_token is not None else None
