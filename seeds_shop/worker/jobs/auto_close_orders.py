from typing import Annotated, Any

from aiogram import Bot
from dishka import FromDishka
from dishka.integrations.arq import inject
from fluentogram import TranslatorRunner

from seeds_shop.core.config import Settings
from seeds_shop.core.models.enums.order import OrderStatus
from seeds_shop.core.services import OrderService, ProductService, UserService
from seeds_shop.tg_bot.keyboards.inline import after_order_kb
from seeds_shop.tg_bot.services.locale import Localizator
from seeds_shop.tg_bot.services.tg_helpers import send_tg_message
from seeds_shop.worker.exception_handler import exception_handler


@exception_handler
@inject
async def free_stock_in_cancelled_orders(
    context: dict[Any, Any],
    bot: Annotated[Bot, FromDishka()],
    config: Annotated[Settings, FromDishka()],
    localizator: Annotated[Localizator, FromDishka()],
    order_service: Annotated[OrderService, FromDishka()],
    user_service: Annotated[UserService, FromDishka()],
    product_service: Annotated[ProductService, FromDishka()],
) -> None:
    """Возвращает в продажу товары из заказов с отмененной оплатой"""
    cancelled_orders = await order_service.get_expired_payment_orders()

    for order in cancelled_orders:
        order_buyer = await user_service.get_user_by_id(order.buyer_db_id)
        locale: TranslatorRunner = localizator.get_by_locale(order_buyer.lang_code)

        for line in order.order_lines:
            await product_service.increase_product_available_quantity(
                order.shop_id, order.delivery_zone_id, line.product_id, line.quantity
            )
        await order_service.update_order_status(order.id, OrderStatus.cancelled)
        await send_tg_message(
            bot,
            order_buyer.telegram_id,
            locale.get("order-cancelled-msg", order_id=order.id),
            reply_markup=after_order_kb(locale),
        )
        # TODO Удалять сообщение выше
        await send_tg_message(
            bot,
            config.tg_bot.admin_channel_id,
            locale.get(
                "order-automatically-cancelled-msg",
                order_id=order.id,
            ),
        )


@exception_handler
@inject
async def auto_close_completed_orders(
    context: dict[Any, Any],
    bot: Annotated[Bot, FromDishka()],
    config: Annotated[Settings, FromDishka()],
    localizator: Annotated[Localizator, FromDishka()],
    order_service: Annotated[OrderService, FromDishka()],
):
    """Автоматически закрываем заказы в статусе in_transit"""

    orders = await order_service.get_completed_orders()
    locale: TranslatorRunner = localizator.get_by_locale("ru")

    for order in orders:
        await send_tg_message(
            bot,
            config.tg_bot.admin_channel_id,
            locale.get(
                "order-automatically-closed-msg",
                order_id=order.id,
            ),
        )
        await order_service.update_order_status(order.id, OrderStatus.closed)
