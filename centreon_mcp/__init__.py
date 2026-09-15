from typing import Literal

from dotenv import load_dotenv
from fastmcp.utilities.logging import get_logger
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = get_logger("centreon")


load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_ignore_empty=True, env_prefix="centreon_")

    mcp_host: str = Field(
        default="localhost", description="Network interface the MCP HTTP server binds to."
    )
    mcp_port: int = Field(default=8000, description="TCP port the MCP HTTP server listens on.")
    mcp_log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Lowest severity level emitted by the MCP service logs."
    )
    base_url: str = Field(
        description="Base URL of the Centreon instance to connect to, "
        "e.g. `https://centreon.example.com`."
    )
    api_token: str | None = Field(
        default=None,
        description="Fallback Centreon API token, used when the MCP client does not supply one "
        "through the `centreon-api-token` header.",
    )
    client_timeout: int = Field(
        default=30, description="Timeout, in seconds, for requests to the Centreon API."
    )
    tls_secure: bool = Field(
        default=True,
        description="Whether to verify the Centreon server's TLS certificate. Set to `False` to "
        "disable TLS certificate verification (insecure, not recommended for production).",
    )
    ca_bundle: str | None = Field(
        default=None,
        description="Path to a custom CA bundle file used to verify the Centreon server's TLS "
        "certificate, e.g. for a self-signed or internal CA. Ignored when `tls_secure` is `False`.",
    )

    @property
    def verify(self) -> bool | str:
        if not self.tls_secure or (self.tls_secure and self.ca_bundle is None):
            return self.tls_secure
        else:
            return self.ca_bundle


settings = Settings()  # type: ignore[call-arg]
