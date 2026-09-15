from typing import Literal

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Search from the working directory, not from this file, which sits in the installed package
load_dotenv(find_dotenv(usecwd=True))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_ignore_empty=True, env_prefix="centreon_")

    mcp_host: str = "localhost"
    mcp_port: int = 8000
    mcp_log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    # Where clients reach this server, which every interactive plugin needs to build its callback
    mcp_public_url: str | None = None
    # Icon and link identifying this server on the consent screen shown before signing in
    mcp_icon_url: str | None = None
    mcp_website_url: str | None = None
    auth_plugin: str = "none"
    base_url: str | None = None
    api_token: str | None = None
    client_timeout: int = 30


settings = Settings()  # type: ignore[call-arg]
