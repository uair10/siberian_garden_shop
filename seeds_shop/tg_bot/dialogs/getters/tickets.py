from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from seeds_shop.core.services import OrderService, TicketService


async def user_tickets_getter(dialog_manager: DialogManager, ticket_service: TicketService, **kwargs):
    user_tickets = await ticket_service.get_user_tickets(dialog_manager.event.from_user.id)

    return {"user_tickets": user_tickets}


async def ticket_info_getter(
    dialog_manager: DialogManager,
    locale: TranslatorRunner,
    ticket_service: TicketService,
    order_service: OrderService,
    **kwargs,
):
    ticket_id: int = dialog_manager.dialog_data.get("ticket_id")

    ticket = await ticket_service.get_ticket_by_id(ticket_id)
    order_status = None
    if ticket.order_id:
        order = await order_service.get_order_by_id(ticket.order_id)
        order_status = order.status

    return {
        "ticket_id": ticket.id,
        "status_value": locale.get(ticket.status.name),
        "order_status": order_status,
        "user_id": ticket.telegram_id,
        "order_id": ticket.order_id,
        "username": ticket.username,
        "was_created": ticket.created_at,
    }
