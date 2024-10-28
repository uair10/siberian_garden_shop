from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from seeds_shop.core.services import OrderService, PaymentMethodService, ProductService, ShopService, UserService
from seeds_shop.core.services.delivery_method import DeliveryMethodService
from seeds_shop.infrastructure.formatters.product import format_product_line


async def user_orders_getter(dialog_manager: DialogManager, order_service: OrderService, **kwargs):
    user_orders = await order_service.get_user_orders(dialog_manager.event.from_user.id)

    return {"user_orders": user_orders}


async def order_info_getter(
    dialog_manager: DialogManager,
    locale: TranslatorRunner,
    order_service: OrderService,
    shop_service: ShopService,
    user_service: UserService,
    product_service: ProductService,
    payment_method_service: PaymentMethodService,
    delivery_method_service: DeliveryMethodService,
    **kwargs,
):
    user_id: int = dialog_manager.event.from_user.id
    order_id: int = dialog_manager.dialog_data.get("order_id")

    order = await order_service.get_order_by_id(order_id)
    order_owner = await user_service.get_user_by_id(order.buyer_db_id)
    payment_method = await payment_method_service.get_payment_method_by_id(order.payment_method_id)
    delivery_method = await delivery_method_service.get_delivery_method_by_id(order.delivery_method_id)

    shop = await shop_service.get_shop_by_id(order.shop_id)

    order_product_lines_text = ""
    for line in order.order_lines:
        product = await product_service.get_product_by_id(line.product_id)
        order_product_lines_text += format_product_line(
            product.title,
            line.quantity * line.final_unit_price,
            product.measurement,
            line.quantity,
        )

    return {
        "order_id": order.id,
        "status": order.status,
        "order_products_text": order_product_lines_text,
        "delivery_method_name": delivery_method.title,
        "delivery_method_duration": delivery_method.duration_days,
        "summ": order.summ,
        "original_summ": order.original_summ,
        "shipping_address": order.shipping_address,
        "buyer_phone": order.buyer_phone,
        "contact_name": order.buyer_name,
        "shop_name": shop.title,
        "shop_address": shop.contact_address,
        "currency": payment_method.currency,
        "currency_translated": locale.get(payment_method.currency.value),
        "currency_symbol": order.currency_symbol,
        "status_value": locale.get(order.status.name),
        "tracking_link": order.tracking_link,
        "is_own_order": order_owner.telegram_id == user_id,
        "bonuses_amount": order.bonuses_amount,
        "comment": order.comment,
        "was_created": order.created_at.date(),
    }


async def unconfirmed_orders_getter(dialog_manager: DialogManager, order_service: OrderService, **kwargs):
    unconfirmed_orders = await order_service.get_orders_for_confirmation()

    return {"unconfirmed_orders": unconfirmed_orders}


async def orders_for_shipping_getter(dialog_manager: DialogManager, order_service: OrderService, **kwargs):
    orders_for_shipping = await order_service.get_orders_for_shipping()

    return {"orders_for_shipping": orders_for_shipping}
