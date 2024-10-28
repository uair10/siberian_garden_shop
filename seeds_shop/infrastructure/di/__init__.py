from seeds_shop.infrastructure.di.arq import ArqProvider
from seeds_shop.infrastructure.di.bot import BotProvider
from seeds_shop.infrastructure.di.config import ConfigProvider
from seeds_shop.infrastructure.di.db import DbProvider, RedisProvider
from seeds_shop.infrastructure.di.localizator import LocalizatorProvider


def get_providers():
    return [
        ConfigProvider(),
        DbProvider(),
        RedisProvider(),
        BotProvider(),
        ArqProvider(),
        LocalizatorProvider(),
    ]
