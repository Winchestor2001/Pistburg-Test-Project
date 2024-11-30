from pathlib import Path

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8001
    domain: str = "https://0.0.0.0:8001"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    version: str = "2.6.1"


class RedisSettings(BaseModel):
    HOST: str = "localhost"
    PORT: int = 6379
    DB: int = 8
    TIMEOUT: int = 10


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class TokenConfig(BaseModel):
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    access_token_expire_minutes: int = 60 * 60 * 24 * 7
    refresh_token_expire_minutes: int = 60 * 60 * 24 * 30
    algorithm: str = "HS256"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",

    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    token: TokenConfig = TokenConfig()
    redis: RedisSettings = RedisSettings()
    db: DatabaseConfig

    log_file_path: str = str(Path(__file__).parent.parent / "logs/debug.log")

    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db: str = ""


settings = Settings()
