from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start

from seeds_shop.core.models.enums.user import UserRole
from seeds_shop.tg_bot.dialogs.getters.users import user_role_getter
from seeds_shop.tg_bot.dialogs.widgets import LocaleText
from seeds_shop.tg_bot.states.admin import AdminSG, BotStatusSG, MailingSG, TicketsSG
from seeds_shop.tg_bot.states.user import ClientSG, UserOrdersSG

features_window = Window(
    LocaleText("select-option-msg"),
    Start(
        LocaleText("send-mailing-btn"),
        id="mailing",
        state=MailingSG.mailing_text,
        when=F["user_role"] == UserRole.admin,
    ),
    Start(
        LocaleText("unconfirmed-orders-btn"),
        id="unconfirmed_orders",
        state=UserOrdersSG.orders_history,
        data={"is_admin": True},
        when=F["user_role"] == UserRole.admin,
    ),
    Start(
        LocaleText("orders-for-shipping-btn"),
        id="orders_for_shipping",
        state=UserOrdersSG.orders_history,
        data={"is_stuff": True},
        when=F["user_role"] == UserRole.stuff,
    ),
    Start(
        LocaleText("tickets-btn"),
        id="opened_tickets",
        state=TicketsSG.tickets_history,
        when=F["user_role"] == UserRole.admin,
    ),
    Start(
        LocaleText("bot-status-btn"),
        "bot_status",
        state=BotStatusSG.display_bot_status,
        when=F["user_role"] == UserRole.admin,
    ),
    Start(
        LocaleText("back-btn"),
        id="back_to_menu",
        state=ClientSG.start,
    ),
    state=AdminSG.admin,
    getter=user_role_getter,
)

features_dialog = Dialog(features_window)
