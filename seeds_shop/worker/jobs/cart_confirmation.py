from typing import Annotated, Any

from aiogram import Bot
from dishka import FromDishka
from dishka.integrations.arq import inject
from fluentogram import TranslatorRunner

from seeds_shop.core.config import Settings
from seeds_shop.core.models.dto.cart import CartDTO
from seeds_shop.core.models.enums.currency import CurrencySymbol
from seeds_shop.core.services import ProductService, PromocodeService, UserService
from seeds_shop.infrastructure.database.redis import TelegramMessageStorage
from seeds_shop.infrastructure.formatters.product import format_product_line
from seeds_shop.tg_bot.keyboards.inline import confirm_cart_kb
from seeds_shop.tg_bot.services.locale import Localizator
from seeds_shop.tg_bot.services.tg_helpers import delete_msg_by_id, send_tg_message
from seeds_shop.worker.exception_handler import exception_handler


@exception_handler
@inject
async def send_cart_confirmation_msg(
    context: dict[Any, Any],
    bot: Annotated[Bot, FromDishka()],
    localizator: Annotated[Localizator, FromDishka()],
    config: Annotated[Settings, FromDishka()],
    user_service: Annotated[UserService, FromDishka()],
    product_service: Annotated[ProductService, FromDishka()],
    promocode_service: Annotated[PromocodeService, FromDishka()],
    message_storage: Annotated[TelegramMessageStorage, FromDishka()],
    user_tg_id: int,
    cart: CartDTO,
) -> None:
    user = await user_service.get_user_by_telegram_id(user_tg_id)

    locale: TranslatorRunner = localizator.get_by_locale(user.lang_code)

    if message := await message_storage.get_last_message(user_tg_id):
        await delete_msg_by_id(bot, message.message_id, message.chat_id)

    promocode = await promocode_service.get_promocode_by_name(cart.promocode)

    txt = locale.get("cart-review-msg")

    for line in cart.lines:
        product = await product_service.get_product_by_id(line.product_id)
        txt += format_product_line(
            line.title,
            (line.quantity * line.final_unit_price),
            product.measurement,
            line.quantity,
        )

    txt += locale.get(
        "cart-total-summ",
        cart_total=cart.total_amount,
        currency_symbol=CurrencySymbol.rub.value,
        bonuses_amount=cart.bonuses_amount,
    )

    txt += locale.get("select-delivery-type")

    if msg := await send_tg_message(
        bot,
        user_tg_id,
        txt,
        reply_markup=confirm_cart_kb(
            locale,
            config.tg_bot.webapp_url,
            promocode_id=promocode.id if promocode else None,
            bonuses_amount=cart.bonuses_amount,
        ),
    ):
        await message_storage.set_last_message(msg)
