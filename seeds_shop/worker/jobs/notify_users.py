from typing import Annotated, Any

from aiogram import Bot, types
from dishka import FromDishka
from dishka.integrations.arq import inject

from seeds_shop.core.config import Settings
from seeds_shop.core.services import UserService
from seeds_shop.tg_bot.services.tg_helpers import broadcast
from seeds_shop.worker.exception_handler import exception_handler


@exception_handler
@inject
async def notify_users(
    context: dict[Any, Any],
    bot: Annotated[Bot, FromDishka()],
    config: Annotated[Settings, FromDishka()],
    user_service: Annotated[UserService, FromDishka()],
    message: types.Message,
) -> None:
    users = await user_service.get_all_users()
    messages_sent, errors_count = await broadcast(bot, users, message)

    await broadcast(
        bot,
        config.tg_bot.admin_ids,
        (
            f"Рассылка закончена\n"
            f"Успешно отправлено сообщений: {messages_sent}\n"
            f"С ошибкой: {errors_count}\n"
            f"Всего пользователей: {len(users)}"
        ),
    )
