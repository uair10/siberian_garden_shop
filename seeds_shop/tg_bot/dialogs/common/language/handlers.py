from typing import Any

from aiogram import types
from aiogram_dialog import DialogManager

from seeds_shop.core.models.enums.user import LangCode
from seeds_shop.core.services import UserService
from seeds_shop.tg_bot.services.locale import Localizator


async def set_user_language(call: types.CallbackQuery, widget: Any, manager: DialogManager, **kwargs):
    user_service: UserService = manager.middleware_data.get("user_service")
    new_lang = getattr(LangCode, widget.widget_id)
    await user_service.change_user_lang(call.from_user.id, new_lang)
    await call.answer("Language changed")

    localizator: Localizator = manager.middleware_data.get("localizator")
    manager.middleware_data["locale"] = localizator.get_by_locale(new_lang)

    await manager.done()
