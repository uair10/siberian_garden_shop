from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Next, ScrollingGroup, Select, Start
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from seeds_shop.tg_bot.dialogs.extras import copy_start_data_to_ctx
from seeds_shop.tg_bot.dialogs.getters.delivery_methods import delivery_method_getter, delivery_methods_getter
from seeds_shop.tg_bot.dialogs.getters.dynamic_media import name_asset_getter, phone_asset_getter
from seeds_shop.tg_bot.dialogs.getters.payments import payment_method_getter, payment_methods_getter
from seeds_shop.tg_bot.dialogs.widgets import LocaleText, SwitchInlineQueryCurrentChat
from seeds_shop.tg_bot.states import ClientSG, CreateOrderSG

from .handlers import (
    create_or_update_order,
    go_back_with_job_cancel,
    process_invoice_screenshot,
    set_city,
    set_delivery_method,
    set_user_contact_name,
    set_user_contact_phone,
    set_user_delivery_address,
    set_user_postal_code,
)

enter_city_window = Window(
    LocaleText("enter-city-msg"),
    SwitchInlineQueryCurrentChat(Const("Выбрать город"), Const("")),
    Start(
        LocaleText("change-cart-btn"),
        id="back_to_menu",
        state=ClientSG.start,
    ),
    TextInput("delivery_city", str, on_success=set_city),
    state=CreateOrderSG.enter_city,
)

select_delivery_method_window = Window(
    LocaleText("select-delivery-method"),
    ScrollingGroup(
        Select(
            Format("{item.title} - {item.price} ₽. Срок доставки (в днях): {item.duration_days}"),
            "delivery_methods_sel",
            lambda method: method.id,
            "delivery_methods",
            on_click=set_delivery_method,
        ),
        width=1,
        height=3,
        id="useritemssel",
        hide_on_single_page=True,
    ),
    Back(LocaleText("back-btn")),
    state=CreateOrderSG.select_delivery_method,
    getter=delivery_methods_getter,
)


enter_contact_name_window = Window(
    LocaleText("enter-name-msg"),
    DynamicMedia(
        "name_hint_video",
        when=F["name_hint_video"],
    ),
    TextInput("contact_name", str, on_success=set_user_contact_name),
    Back(LocaleText("back-btn")),
    state=CreateOrderSG.enter_contact_name,
    getter=name_asset_getter,
)

enter_phone_window = Window(
    LocaleText("enter-phone-msg"),
    DynamicMedia(
        "phone_hint_video",
        when=F["phone_hint_video"],
    ),
    TextInput("contact_phone", str, on_success=set_user_contact_phone),
    Back(LocaleText("back-btn")),
    state=CreateOrderSG.enter_phone,
    getter=phone_asset_getter,
)

enter_address_window = Window(
    LocaleText("enter-address-msg"),
    TextInput("delivery_address", str, on_success=set_user_delivery_address),
    Back(LocaleText("back-btn")),
    state=CreateOrderSG.enter_address,
)

enter_postal_code_window = Window(
    LocaleText("enter-postal-code-msg"),
    TextInput("postal_code", str, on_success=set_user_postal_code),
    Back(LocaleText("back-btn")),
    state=CreateOrderSG.enter_postal_code,
)

show_delivery_message = Window(
    Format("{accompanying_message}"),
    Next(LocaleText("continue-btn")),
    state=CreateOrderSG.show_delivery_message,
    getter=delivery_method_getter,
)

select_payment_method_window = Window(
    LocaleText("select-payment-method-msg"),
    ScrollingGroup(
        Select(
            Format("{item.currency}"),
            "payment_method_sel",
            lambda method: method.id,
            "payment_methods",
            on_click=create_or_update_order,
        ),
        width=2,
        height=3,
        id="useritemssel",
        hide_on_single_page=True,
    ),
    Back(LocaleText("back-btn")),
    state=CreateOrderSG.select_payment_method,
    getter=payment_methods_getter,
)

send_invoice_screenshot_window = Window(
    DynamicMedia("payment_image", when=F["payment_image"]),
    LocaleText(
        "send-invoice-screenshot-msg",
        summ="{dialog_data[order_summ]}",
        delivery_cost="{dialog_data[delivery_cost]}",
        currency="{currency}",
        payment_address="{payment_address}",
    ),
    Format("{dialog_data[order_product_lines_text]}"),
    MessageInput(process_invoice_screenshot, content_types=ContentType.ANY),
    Button(
        LocaleText("back-btn"),
        id="back_with_job_cancel_btn",
        on_click=go_back_with_job_cancel,
    ),
    state=CreateOrderSG.send_invoice_screenshot,
    getter=payment_method_getter,
)

create_order_dialog = Dialog(
    enter_city_window,
    select_delivery_method_window,
    enter_contact_name_window,
    enter_phone_window,
    enter_address_window,
    enter_postal_code_window,
    show_delivery_message,
    select_payment_method_window,
    send_invoice_screenshot_window,
    on_start=copy_start_data_to_ctx,
)
