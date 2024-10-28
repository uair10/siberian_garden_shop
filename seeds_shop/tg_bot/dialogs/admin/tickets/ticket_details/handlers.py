from typing import Any

from aiogram import Bot, types
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from seeds_shop.core.config import Settings
from seeds_shop.core.models.enums.order import OrderStatus
from seeds_shop.core.services import OrderService, ProductService, TicketService, UserService
from seeds_shop.tg_bot.services.tg_helpers import send_tg_message


async def close_ticket(call: types.CallbackQuery, _, manager: DialogManager):
    """Закрываем тикет"""

    bot: Bot = manager.middleware_data.get("bot")
    locale: TranslatorRunner = manager.middleware_data.get("locale")
    config: Settings = manager.middleware_data.get("config")
    ticket_service: TicketService = manager.middleware_data.get("ticket_service")

    ticket_id: int = manager.dialog_data.get("ticket_id")

    await ticket_service.close_ticket(ticket_id)

    await send_tg_message(
        bot,
        config.tg_bot.admin_channel_id,
        locale.get(
            "ticket-was-closed-msg",
            ticket_id=ticket_id,
            admin_id=str(call.from_user.id),
        ),
    )

    await call.answer(locale.get("ticket-closed-msg"))

    await manager.done()


async def update_order_from_ticket(call: types.CallbackQuery, widget: Any, manager: DialogManager):
    """Закрываем / отменяем заказ"""

    bot: Bot = manager.middleware_data.get("bot")
    locale: TranslatorRunner = manager.middleware_data.get("locale")
    config: Settings = manager.middleware_data.get("config")
    ticket_service: TicketService = manager.middleware_data.get("ticket_service")
    order_service: OrderService = manager.middleware_data.get("order_service")
    product_service: ProductService = manager.middleware_data.get("product_service")
    user_service: UserService = manager.middleware_data.get("user_service")

    ticket_id: int = manager.dialog_data.get("ticket_id")
    ticket = await ticket_service.get_ticket_by_id(ticket_id)

    order = await order_service.get_order_by_id(ticket.order_id)
    order_buyer = await user_service.get_user_by_id(order.user_id)

    if widget.widget_id == "close":
        new_status = OrderStatus.closed
        user_msg = locale.get("order-closed-msg", order_id=order.id)
        admin_msg = locale.get("ticket-order-closed-msg")
    else:
        new_status = OrderStatus.cancelled
        user_msg = locale.get("order-cancelled-msg", order_id=order.id)
        admin_msg = locale.get("ticket-order-cancelled-msg")

    await order_service.update_order_status(ticket.order_id, new_status)
    for line in order.order_lines:
        await product_service.increase_product_available_quantity(order.shop_id, line.product_id, line.quantity)
    await send_tg_message(bot, order_buyer.telegram_id, user_msg)

    await send_tg_message(
        bot,
        config.tg_bot.admin_channel_id,
        locale.get(
            "order-status-changed-msg",
            order_id=ticket.order_id,
            status=new_status.value,
        ),
    )

    await call.answer(admin_msg)

    await manager.done()
