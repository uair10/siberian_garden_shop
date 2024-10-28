from dishka import Provider, Scope, provide

from seeds_shop.core.config import DbConfig, RedisConfig, Settings, TgBotConfig
from seeds_shop.infrastructure.config_loader import load_config


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_config(self) -> Settings:
        return load_config(Settings)

    @provide
    def get_db_config(self, config: Settings) -> DbConfig:
        return config.db

    @provide
    def get_redis_config(self, config: Settings) -> RedisConfig:
        return config.redis

    @provide
    def get_tg_bot_config(self, config: Settings) -> TgBotConfig:
        return config.tg_bot
