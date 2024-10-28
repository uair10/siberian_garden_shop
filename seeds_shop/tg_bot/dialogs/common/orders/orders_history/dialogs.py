from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format

from seeds_shop.tg_bot.dialogs.getters.orders import (
    orders_for_shipping_getter,
    unconfirmed_orders_getter,
    user_orders_getter,
)
from seeds_shop.tg_bot.dialogs.widgets import LocaleText
from seeds_shop.tg_bot.states import UserOrdersSG

from .handlers import display_order_details

orders_history_window = Window(
    LocaleText(
        "orders-history-msg",
        when=(~F["start_data"]["is_admin"]) & (~F["start_data"]["is_stuff"]),
    ),
    LocaleText("unconfirmed-orders-msg", when=F["start_data"]["is_admin"]),
    LocaleText("orders-for-shipping-msg", when=F["start_data"]["is_stuff"]),
    ScrollingGroup(
        Select(
            Format("№{item.id} {item.summ} {item.currency_symbol} {item.created_at}"),
            "user_orders_sel",
            lambda order: order.id,
            "user_orders",
            on_click=display_order_details,
            when=(~F["start_data"]["is_admin"]) & (~F["start_data"]["is_stuff"]),
        ),
        Select(
            Format("№{item.id} {item.summ} {item.currency_symbol} {item.created_at}"),
            "orders_sel",
            lambda order: order.id,
            "unconfirmed_orders",
            on_click=display_order_details,
            when=F["start_data"]["is_admin"],
        ),
        Select(
            Format("№{item.id} {item.summ} {item.currency_symbol} {item.created_at}"),
            "orders_sel",
            lambda order: order.id,
            "orders_for_shipping",
            on_click=display_order_details,
            when=F["start_data"]["is_stuff"],
        ),
        width=1,
        height=4,
        id="useritemssel",
        hide_on_single_page=True,
    ),
    Cancel(
        LocaleText("back-btn"),
    ),
    state=UserOrdersSG.orders_history,
    getter=(user_orders_getter, unconfirmed_orders_getter, orders_for_shipping_getter),
)

orders_history_dialog = Dialog(
    orders_history_window,
)
