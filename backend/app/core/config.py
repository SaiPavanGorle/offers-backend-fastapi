from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Proximity Offers Backend"
    app_env: str = "dev"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/offers_db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
