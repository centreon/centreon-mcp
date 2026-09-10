from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_ignore_empty=True, env_prefix="centreon_")

    mcp_host: str = "localhost"
    mcp_port: int = 8000
    mcp_log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    base_url: str
    api_token: str | None = None
    client_timeout: int = 30


settings = Settings()  # type: ignore[call-arg]
