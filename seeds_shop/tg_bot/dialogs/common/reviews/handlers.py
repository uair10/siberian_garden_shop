from aiogram import types
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from seeds_shop.core.services import UserService
from seeds_shop.tg_bot.services.tg_helpers import answer_msg_with_autodelete


async def leave_review(message: types.Message, _, manager: DialogManager, review_text: str):
    locale: TranslatorRunner = manager.middleware_data.get("locale")
    user_service: UserService = manager.middleware_data.get("user_service")

    await user_service.create_user_review(message.from_user.id, review_text)

    await answer_msg_with_autodelete(message, locale.get("thanks-for-review-msg"))

    await manager.done()
