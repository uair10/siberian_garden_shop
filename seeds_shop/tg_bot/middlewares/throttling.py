from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        caches = {"default": TTLCache(maxsize=10_000, ttl=data["config"].tg_bot.throttle_time)}
        throttling_key = get_flag(data, "throttling_key")
        if throttling_key is not None and throttling_key in caches:
            if event.chat.id in caches[throttling_key]:
                return None
            else:
                caches[throttling_key][event.chat.id] = None
        return await handler(event, data)
