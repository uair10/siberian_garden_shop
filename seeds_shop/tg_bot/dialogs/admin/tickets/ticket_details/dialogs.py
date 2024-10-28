from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Next, SwitchTo

from seeds_shop.core.models.enums.order import OrderStatus
from seeds_shop.tg_bot.dialogs.extras import copy_start_data_to_ctx
from seeds_shop.tg_bot.dialogs.getters.tickets import ticket_info_getter
from seeds_shop.tg_bot.dialogs.widgets import LocaleText
from seeds_shop.tg_bot.states.admin import TicketDetailsSG

from .handlers import close_ticket, update_order_from_ticket

ticket_details_window = Window(
    LocaleText("ticket-overview"),
    LocaleText("ticket-id", ticket_id="{ticket_id}"),
    LocaleText("ticket-status", status="{status_value}"),
    LocaleText("ticket-order-id", order_id="{order_id}", when=F["order_id"]),
    LocaleText("ticket-user-id", user_id="{user_id}"),
    LocaleText("ticket-user-username", username="{username}"),
    LocaleText("was-created", was_created="{was_created}"),
    Next(
        LocaleText("close-ticket-btn"),
    ),
    SwitchTo(
        LocaleText("close-order-btn"),
        "close_order_btn",
        state=TicketDetailsSG.confirm_closing_order,
        when=(F["order_status"]) & (F["order_status"] != OrderStatus.closed),
    ),
    SwitchTo(
        LocaleText("cancel-order-btn"),
        "cancel_order_btn",
        state=TicketDetailsSG.confirm_cancel_order,
        when=(F["order_status"]) & (F["order_status"] != OrderStatus.cancelled),
    ),
    Cancel(LocaleText("back-btn")),
    state=TicketDetailsSG.ticket_details,
    getter=ticket_info_getter,
)

confirm_closing_ticket_window = Window(
    LocaleText("confirm-closing-ticket-msg"),
    Button(LocaleText("confirm-btn"), id="close_ticket", on_click=close_ticket),
    Back(LocaleText("back-btn")),
    state=TicketDetailsSG.confirm_closing_ticket,
)

confirm_closing_order_window = Window(
    LocaleText("confirm-closing-order-msg"),
    Button(LocaleText("confirm-btn"), id="close", on_click=update_order_from_ticket),
    SwitchTo(LocaleText("back-btn"), "back_to_details", state=TicketDetailsSG.ticket_details),
    state=TicketDetailsSG.confirm_closing_order,
)

confirm_cancel_order_window = Window(
    LocaleText("confirm-canceling-order-msg"),
    Button(LocaleText("confirm-btn"), id="cancel", on_click=update_order_from_ticket),
    SwitchTo(LocaleText("back-btn"), "back_to_details", state=TicketDetailsSG.ticket_details),
    state=TicketDetailsSG.confirm_cancel_order,
)


ticket_details_dialog = Dialog(
    ticket_details_window,
    confirm_closing_ticket_window,
    confirm_closing_order_window,
    confirm_cancel_order_window,
    on_start=copy_start_data_to_ctx,
)
