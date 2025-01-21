from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=("sample.env", ".env"), env_file_encoding="utf-8")

    CH_HOST: str = "some-clickhouse-host"
    CH_USERNAME: str = "some-clickhouse-username"
    CH_PASSWORD: str = "some-clickhouse-password"

    NATS_HOST: str = "some-nats-host"
    NATS_PORT: str = "some-nats-port"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
