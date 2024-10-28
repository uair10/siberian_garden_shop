from aiogram_dialog import DialogManager

from seeds_shop.tg_bot.states.admin import TicketDetailsSG


async def display_ticket_details(_, __, manager: DialogManager, ticket_id: str):
    await manager.start(TicketDetailsSG.ticket_details, {"ticket_id": int(ticket_id)})
