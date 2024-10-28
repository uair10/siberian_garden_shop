from aiogram import Bot, types
from aiogram.filters.callback_data import CallbackData
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from seeds_shop.core.config import Settings
from seeds_shop.core.models.enums.user import UserRole
from seeds_shop.core.services import OrderService, StatsService, TicketService, UserService
from seeds_shop.tg_bot.keyboards.inline import take_ticket_btn
from seeds_shop.tg_bot.services.tg_helpers import answer_msg_with_autodelete, broadcast, delete_msg, send_tg_message
from seeds_shop.tg_bot.states.admin import TicketDetailsSG


async def contact_support(
    call: types.CallbackQuery,
    callback_data: CallbackData,
    dialog_manager: DialogManager,
):
    """Создание тикета пользователем"""

    bot: Bot = dialog_manager.middleware_data.get("bot")
    config: Settings = dialog_manager.middleware_data.get("config")
    locale: TranslatorRunner = dialog_manager.middleware_data.get("locale")
    user_service: UserService = dialog_manager.middleware_data.get("user_service")
    ticket_service: TicketService = dialog_manager.middleware_data.get("ticket_service")
    stats_service: StatsService = dialog_manager.middleware_data.get("stats_service")
    order_service: OrderService = dialog_manager.middleware_data.get("order_service")

    order_id: int = dialog_manager.dialog_data.get("order_id")
    if not order_id:
        order_id = callback_data.order_id
        if not order_id:
            return

    username = call.from_user.username
    if not username:
        username = call.from_user.full_name

    ticket = await ticket_service.create_ticket(call.from_user.id, username, order_id)

    order = await order_service.get_order_by_id(order_id)

    # Отправляем тикет админам магазина
    admins = await user_service.get_users_by_role_and_shop_id(UserRole.admin, order.shop_id)
    admin_msg = locale.get(
        "new-ticket-msg",
        ticket_id=ticket.id,
        user_id=str(call.from_user.id),
        shop_id=order.shop_id,
    )
    await send_tg_message(bot, config.tg_bot.admin_channel_id, admin_msg)
    await broadcast(
        bot,
        admins,
        admin_msg,
        reply_markup=take_ticket_btn(locale, ticket_id=ticket.id),
    )

    await stats_service.add_stats(tickets_opened=1)
    await answer_msg_with_autodelete(call.message, locale.get("ticket-sent-msg"))


async def take_ticket(
    call: types.CallbackQuery,
    callback_data: CallbackData,
    dialog_manager: DialogManager,
):
    """Взятие тикета в работу"""

    bot: Bot = dialog_manager.middleware_data.get("bot")
    config: Settings = dialog_manager.middleware_data.get("config")
    locale: TranslatorRunner = dialog_manager.middleware_data.get("locale")
    ticket_service: TicketService = dialog_manager.middleware_data.get("ticket_service")

    ticket_id: int = callback_data.ticket_id
    ticket = await ticket_service.get_ticket_by_id(ticket_id)
    if ticket.admin:
        await call.answer(locale.get("ticket-already-taken", admin_id=str(ticket.admin.telegram_id)))
        return

    await ticket_service.assign_ticket_to_admin(ticket_id, call.from_user.id)
    await send_tg_message(
        bot,
        config.tg_bot.admin_channel_id,
        locale.get(
            "ticket-assigned-by-admin-msg",
            ticket_id=ticket_id,
            admin_id=str(call.from_user.id),
        ),
    )

    await call.answer(locale.get("ticket-taken-msg"))
    await delete_msg(call.message)

    await dialog_manager.start(
        TicketDetailsSG.ticket_details,
        data={"ticket_id": callback_data.ticket_id},
    )
