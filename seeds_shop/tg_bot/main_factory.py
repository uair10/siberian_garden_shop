from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisEventIsolation, RedisStorage
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.protocols import MessageManagerProtocol
from aiogram_dialog.manager.message_manager import MessageManager
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from redis.asyncio import Redis

from seeds_shop.core.config import Settings, TgBotConfig
from seeds_shop.infrastructure.database.factory import create_redis
from seeds_shop.infrastructure.di import get_providers
from seeds_shop.tg_bot.dialogs import register_dialogs
from seeds_shop.tg_bot.handlers import register_handlers
from seeds_shop.tg_bot.middlewares import setup_middlewares


def create_container() -> AsyncContainer:
    container = make_async_container(*get_bot_providers())
    return container


def get_bot_providers() -> list[Provider]:
    return [
        *get_providers(),
        *get_bot_specific_providers(),
    ]


def get_bot_specific_providers() -> list[Provider]:
    return [
        DpProvider(),
        DialogManagerProvider(),
    ]


class DialogManagerProvider(Provider):
    scope = Scope.APP

    @provide
    def get_manager(self) -> MessageManagerProtocol:
        return MessageManager()


class DpProvider(Provider):
    scope = Scope.APP

    @provide
    def create_dispatcher(
        self,
        container: AsyncContainer,
        event_isolation: BaseEventIsolation,
        bot_config: TgBotConfig,
        storage: BaseStorage,
    ) -> Dispatcher:
        dp = Dispatcher(
            storage=storage,
            events_isolation=event_isolation,
        )
        setup_middlewares(
            container=container,
            dp=dp,
        )
        setup_dialogs(dp)
        register_dialogs(dp)
        register_handlers(dp, bot_config)

        return dp

    @provide
    def create_storage(self, config: Settings) -> BaseStorage:
        if config.tg_bot.use_redis:
            return RedisStorage(create_redis(config.redis), key_builder=DefaultKeyBuilder(with_destiny=True))
        return MemoryStorage()

    @provide
    def get_event_isolation(self, redis: Redis) -> BaseEventIsolation:
        return RedisEventIsolation(redis)


def resolve_update_types(dp: Dispatcher) -> list[str]:
    return dp.resolve_used_update_types(skip_events={"aiogd_update"})
