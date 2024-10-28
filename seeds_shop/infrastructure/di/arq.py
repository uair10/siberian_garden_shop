from typing import AsyncGenerator

from arq import ArqRedis, create_pool
from dishka import Provider, Scope, provide

from seeds_shop.core.config import RedisConfig


class ArqProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_arq(self, redis_config: RedisConfig) -> AsyncGenerator[ArqRedis, None]:
        yield await create_pool(redis_config.pool_settings)
