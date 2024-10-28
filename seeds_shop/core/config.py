import json
import logging

from arq.connections import RedisSettings
from pydantic import BaseModel
from pydantic.v1 import validator


class DbConfig(BaseModel):
    host: str
    port: int
    name: str
    user: str
    password: str
    echo: bool = False

    def full_url(self, with_driver: bool = True) -> str:
        login_data = f"{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        if with_driver:
            return f"postgresql+asyncpg://{login_data}"
        return f"postgresql://{login_data}"


class RedisConfig(BaseModel):
    host: str
    port: int
    database: int

    @property
    def url(self) -> str:
        return f"redis://@{self.host}:{self.port}/{self.database}"

    @property
    def pool_settings(self) -> RedisSettings:
        return RedisSettings(
            host=self.host,
            port=self.port,
            database=self.database,
        )


class ApiConfig(BaseModel):
    host: str
    port: int
    allowed_origins: list[str]
    allowed_hosts: list[str]
    debug: bool = False
    log_level: str | int = logging.DEBUG

    @validator("allowed_origins", "allowed_hosts", pre=True, always=True)
    def allowed_origins_hosts_list(cls, v) -> list[str]:
        return json.loads(v)


class TgBotConfig(BaseModel):
    token: str
    admin_ids: list[int]
    developer_id: int
    admin_channel_id: int
    use_redis: bool
    webapp_url: str
    throttle_time: int = 1

    @validator("admin_ids", pre=True, always=True)
    def admin_ids_list(cls, v) -> list[str]:
        return [item.strip() for item in v[1:-1].split(",")]


class Settings(BaseModel):
    tg_bot: TgBotConfig
    db: DbConfig
    redis: RedisConfig
    api: ApiConfig
