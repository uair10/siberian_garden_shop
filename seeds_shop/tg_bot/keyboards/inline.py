from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner


class ConfirmCartCF(CallbackData, prefix="confirmcart"):
    bonuses_amount: int
    promocode_id: int | None = None


def confirm_cart_kb(
    locale: TranslatorRunner,
    webapp_url: str,
    bonuses_amount: int,
    promocode_id: int | None = None,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=locale.get("delivery-btn"),
        callback_data=ConfirmCartCF(promocode_id=promocode_id, bonuses_amount=bonuses_amount),
    )
    builder.button(text=locale.get("change-cart-btn"), web_app=WebAppInfo(url=webapp_url))

    builder.adjust(1)

    return builder.as_markup()


class OrderCF(CallbackData, prefix="ordernum"):
    action: str
    order_id: int


class TicketCF(CallbackData, prefix="ticketnum"):
    ticket_id: int


class SupportCF(CallbackData, prefix="supportnum"):
    order_id: int


def expired_payment_kb(
    locale: TranslatorRunner,
    order_id: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=locale.get("go-to-shopping-btn"),
        callback_data="go_to_shopping",
    )
    builder.button(
        text=locale.get("contact-support-btn"),
        callback_data=SupportCF(order_id=order_id),
    )

    builder.adjust(1)

    return builder.as_markup()


def order_payment_confirmation_kb(locale: TranslatorRunner, order_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для подтверждения оплаты заказа"""

    builder = InlineKeyboardBuilder()
    builder.button(
        text=locale.get("go-to-order-btn"),
        callback_data=OrderCF(action="go_to_order", order_id=order_id),
    )

    return builder.as_markup()


def order_shipping_kb(locale: TranslatorRunner, order_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для отгрузки заказа"""

    builder = InlineKeyboardBuilder()
    builder.button(
        text=locale.get("go-to-order-btn"),
        callback_data=OrderCF(action="go_to_order", order_id=order_id),
    )
    builder.button(text=locale.get("hold-off-btn"), callback_data="hold_off")

    builder.adjust(1)

    return builder.as_markup()


def take_ticket_btn(locale: TranslatorRunner, ticket_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=locale.get("take-ticket-btn"), callback_data=TicketCF(ticket_id=ticket_id))

    return builder.as_markup()


def after_order_kb(locale: TranslatorRunner):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=locale.get("go-to-shopping-btn"),
        callback_data="go_to_shopping",
    )

    builder.adjust(1)

    return builder.as_markup()


def go_to_shopping_kb(locale: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=locale.get("go-to-shopping-btn"),
        callback_data="go_to_shopping",
    )

    builder.adjust(1)

    return builder.as_markup()


def calalog_btn_kb(locale: TranslatorRunner, webapp_url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=locale.get("catalog-btn"), web_app=WebAppInfo(url=webapp_url))
    builder.adjust(1)

    return builder.as_markup()
