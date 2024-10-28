from typing import Annotated, Any

from aiogram import Bot, types
from aiogram.types import InlineKeyboardMarkup
from dishka import FromDishka
from dishka.integrations.arq import inject

from seeds_shop.tg_bot.services.tg_helpers import send_tg_message
from seeds_shop.worker.exception_handler import exception_handler


@exception_handler
@inject
async def notify_user(
    context: dict[Any, Any],
    bot: Annotated[Bot, FromDishka()],
    user_tg_id: int,
    text: str,
    reply_markup: types.ReplyKeyboardMarkup | types.InlineKeyboardMarkup | str | None = None,
) -> None:
    if isinstance(reply_markup, str):
        reply_markup = InlineKeyboardMarkup.model_validate_json(reply_markup)

    await send_tg_message(bot, user_tg_id, text, reply_markup=reply_markup)
