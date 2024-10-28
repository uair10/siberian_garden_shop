from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Next, SwitchTo
from aiogram_dialog.widgets.media import DynamicMedia

from seeds_shop.core.models.enums.currency import CurrencySymbol
from seeds_shop.core.models.enums.order import OrderStatus
from seeds_shop.core.models.enums.user import UserRole
from seeds_shop.tg_bot.dialogs.extras import copy_start_data_to_ctx
from seeds_shop.tg_bot.dialogs.getters.media import invoice_screenshot_getter
from seeds_shop.tg_bot.dialogs.getters.orders import order_info_getter
from seeds_shop.tg_bot.dialogs.getters.users import user_role_getter
from seeds_shop.tg_bot.dialogs.widgets import LocaleText
from seeds_shop.tg_bot.states import OrderDetailsSG

from .handlers import change_order_tracking_link, close_order, confirm_order_payment, process_tracking_link

order_details_window = Window(
    LocaleText(
        "prepaid-delivery-order",
    ),
    DynamicMedia(
        "invoice_screenshot",
        when=(F["user_role"] == UserRole.admin) & (F["invoice_screenshot"]) & (~F["is_own_order"]),
    ),
    LocaleText("order-id", order_id="{order_id}"),
    LocaleText("order-status", status="{status_value}"),
    LocaleText("order-summ", summ="{summ}", when=F["user_role"] != UserRole.stuff),
    LocaleText(
        "order-summ",
        summ="{original_summ}",
        currency_symbol=CurrencySymbol.rub.value,
        when=(F["original_summ"]) & (F["user_role"] == UserRole.stuff),
    ),
    LocaleText("order-payment-method", currency="{currency_translated}"),
    LocaleText("order-delivery-method", delivery_method="{delivery_method_name}"),
    LocaleText("order-delivery-duration", delivery_duration="{delivery_method_duration}"),
    LocaleText("order-shipping-address", shipping_address="{shipping_address}", when=F["shipping_address"]),
    LocaleText(
        "order-user-phone",
        user_phone="{buyer_phone}",
        when=(F["buyer_phone"]) & (F["user_role"] != UserRole.user),
    ),
    LocaleText(
        "order-contact-name",
        contact_name="{buyer_name}",
        when=(F["buyer_name"]) & (F["user_role"] != UserRole.user),
    ),
    LocaleText("order-tracking-link", tracking_link="{tracking_link}", when=F["tracking_link"]),
    LocaleText("bonuses-used", bonuses_amount="{bonuses_amount}", when=F["bonuses_amount"]),
    LocaleText(
        "order-comment",
        comment="{comment}",
        when=F["comment"],
    ),
    LocaleText("was-created", was_created="{was_created}"),
    LocaleText("order-products", order_products="{order_products_text}"),
    Next(
        LocaleText("confirm-order-payment-btn"),
        when=(F["user_role"] == UserRole.admin)
        & (~F["is_own_order"])
        & (F["status"] == OrderStatus.payment_not_confirmed),
    ),
    SwitchTo(
        LocaleText("send-tracking-link-btn"),
        "send_tracking_link",
        state=OrderDetailsSG.send_tracking_link,
        when=(F["user_role"] == UserRole.stuff) & (~F["is_own_order"]) & (F["status"] == OrderStatus.payment_confirmed),
    ),
    Button(
        LocaleText("close-order-btn"),
        "close_order_btn",
        on_click=close_order,
        when=(F["user_role"] == UserRole.stuff) & (F["status"] == OrderStatus.in_transit),
    ),
    Cancel(LocaleText("back-btn")),
    state=OrderDetailsSG.order_details,
    getter=(order_info_getter, invoice_screenshot_getter, user_role_getter),
)

confirm_order_window = Window(
    LocaleText("confirm-order-payment-msg"),
    Button(LocaleText("confirm-btn"), id="confirm_payment", on_click=confirm_order_payment),
    Back(LocaleText("back-btn")),
    state=OrderDetailsSG.confirm_order_payment,
)

send_order_tracking_link_window = Window(
    LocaleText("waiting-tracking-link-msg"),
    TextInput("tracking_link", str, on_success=process_tracking_link),
    SwitchTo(LocaleText("back-btn"), "back_to_order", state=OrderDetailsSG.order_details),
    state=OrderDetailsSG.send_tracking_link,
)

confirm_tracking_link_window = Window(
    LocaleText("tracking-link-confirmation-msg", tracking_link="{dialog_data[tracking_link]}"),
    Button(LocaleText("yes-btn"), "confirm_btn", on_click=change_order_tracking_link),
    Back(LocaleText("no-btn")),
    state=OrderDetailsSG.confirm_tracking_link,
)

order_details_dialog = Dialog(
    order_details_window,
    confirm_order_window,
    send_order_tracking_link_window,
    confirm_tracking_link_window,
    on_start=copy_start_data_to_ctx,
)
