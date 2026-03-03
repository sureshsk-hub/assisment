"""
Application settings, pulled from the ENV and from dotenv file (.env)
Intended to hold secrets and important application configurations.

export any of the application settings as an ENV var and they will be pulled in at runtime, for instance...
> export APP_NAME="My Notes API"
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Will read ENV vars first, ./.env file second
    # https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    # Application settings:
    app_name: str = "Notes API"
    sqlachemy_url: str
    sqlachemy_connection_args: dict[str, str | int | float | bool] = {}


@lru_cache()
def get_settings():
    return Settings()  # type: ignore (args will be pulled from ENV & .env)
