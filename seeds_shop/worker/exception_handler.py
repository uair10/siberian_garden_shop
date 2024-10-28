import logging
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from aiogram import Bot
from dishka import AsyncContainer

from seeds_shop.core.config import TgBotConfig
from seeds_shop.tg_bot.services.tg_helpers import send_tg_message

Param = ParamSpec("Param")
ReturnType = TypeVar("ReturnType")
Func = Callable[Param, ReturnType]

logger = logging.getLogger(__name__)


def exception_handler(
    func: Callable[Param, Coroutine[Any, Any, ReturnType]],
) -> Callable[Param, Coroutine[Any, Any, ReturnType]]:
    @wraps(func)
    async def wrapped(*args: Param.args, **kwargs: Param.kwargs) -> ReturnType:
        try:
            return await func(*args, **kwargs)
        except Exception as err:
            container: AsyncContainer = args[0].get("dishka_app_container")
            bot = await container.get(Bot)
            bot_config = await container.get(TgBotConfig)
            logger.exception(f"Error handling job {func}. Error: {err!s}. Args: {args}. Kwargs: {kwargs}")
            await send_tg_message(
                bot,
                bot_config.developer_id,
                f"Ошибка во время выполнения функции планировщика {func.__name__}: {err!s}",
            )

    return wrapped
