from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format

from seeds_shop.tg_bot.dialogs.getters.tickets import user_tickets_getter
from seeds_shop.tg_bot.dialogs.widgets import LocaleText
from seeds_shop.tg_bot.states.admin import TicketsSG

from .handlers import display_ticket_details

tickets_history_window = Window(
    LocaleText(
        "tickets-history-msg",
    ),
    ScrollingGroup(
        Select(
            Format("№{item.id} от {item.telegram_id} {item.created_at}"),
            "user_tickets_sel",
            lambda ticket: ticket.id,
            "user_tickets",
            on_click=display_ticket_details,
        ),
        width=1,
        height=4,
        id="useritemssel",
        hide_on_single_page=True,
    ),
    Cancel(
        LocaleText("back-btn"),
    ),
    state=TicketsSG.tickets_history,
    getter=user_tickets_getter,
)

tickets_history_dialog = Dialog(
    tickets_history_window,
)
