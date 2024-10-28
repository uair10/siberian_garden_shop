from typing import Annotated, Any

from aiogram import Bot
from dishka import FromDishka
from dishka.integrations.arq import inject
from fluentogram import TranslatorRunner

from seeds_shop.core.models.enums.order import OrderStatus
from seeds_shop.core.services import OrderService, UserService
from seeds_shop.infrastructure.database.redis import TelegramMessageStorage
from seeds_shop.tg_bot.keyboards.inline import expired_payment_kb
from seeds_shop.tg_bot.services.locale import Localizator
from seeds_shop.tg_bot.services.tg_helpers import delete_msg_by_id, send_tg_message
from seeds_shop.worker.exception_handler import exception_handler


@exception_handler
@inject
async def notify_expired_payment(
    context: dict[Any, Any],
    bot: Annotated[Bot, FromDishka()],
    localizator: Annotated[Localizator, FromDishka()],
    user_service: Annotated[UserService, FromDishka()],
    order_service: Annotated[OrderService, FromDishka()],
    message_storage: Annotated[TelegramMessageStorage, FromDishka()],
    user_tg_id: int,
    order_id: int,
) -> None:
    """Отправляем сообщение о просроченной оплате"""

    user = await user_service.get_user_by_telegram_id(user_tg_id)
    locale: TranslatorRunner = localizator.get_by_locale(user.lang_code)

    # Удаляем сообщение о истекающей оплате
    if message := await message_storage.get_last_message(user_tg_id):
        await delete_msg_by_id(bot, message.message_id, message.chat_id)

    order = await order_service.get_order_by_id(order_id)
    if order and order.status == OrderStatus.created:
        await order_service.update_order_status(order_id, OrderStatus.payment_canceled)

        await send_tg_message(
            bot,
            user_tg_id,
            locale.get("payment-time-expired-msg"),
            reply_markup=expired_payment_kb(locale, order_id),
        )
