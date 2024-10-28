from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, ErrorEvent, Message, Update

from seeds_shop.core.exceptions.user import UserTgIdNotExist
from seeds_shop.core.models.enums.user import LangCode
from seeds_shop.core.services import UserService


class LocaleMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Message | Update | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        user_service: UserService = data["user_service"]
        if isinstance(event, Update):
            if event.message:
                user_id = event.message.from_user.id
            elif event.inline_query:
                user_id = event.inline_query.from_user.id
            else:
                user_id = event.callback_query.from_user.id
        elif isinstance(event, ErrorEvent):
            if event.update.message:
                user_id = event.update.message.from_user.id
            elif event.update.inline_query:
                user_id = event.update.inline_query.from_user.id
            else:
                user_id = event.update.callback_query.from_user.id
        else:
            user_id = event.from_user.id

        try:
            user = await user_service.get_user_by_telegram_id(user_id)
            user_lang = user.lang_code.value
        except UserTgIdNotExist:
            user_lang = LangCode.en

        data["locale"] = data["localizator"].get_by_locale(user_lang)

        return await handler(event, data)
