import os
from typing import Literal

from dotenv import load_dotenv
from fastmcp.utilities.logging import get_logger
from pydantic import Field, model_validator
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
    mcp_website_url: str | None = Field(
        default=None,
        description="URL to a website with more information about your server. Displayed in client applications",
    )
    auth_plugin: str = Field(
        default="none",
        description="Name of the authentication plugin to load, among those registered under the "
        "`centreon_mcp.auth` entry-point group.",
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
        if not self.tls_secure or self.ca_bundle is None:
            return self.tls_secure
        return self.ca_bundle

    @model_validator(mode="after")
    def _check_ca_bundle_exists(self) -> "Settings":
        if self.tls_secure and self.ca_bundle and not os.path.exists(self.ca_bundle):
            raise ValueError(
                f"CENTREON_CA_BUNDLE='{self.ca_bundle}' does not exist. Fix the path, unset "
                "CENTREON_CA_BUNDLE to use the system CA trust store, or set "
                "CENTREON_TLS_SECURE=False to disable TLS certificate verification."
            )
        return self


settings = Settings()  # type: ignore[call-arg]
