from seeds_shop.core.models.dto.cart import CartLineDTO
from seeds_shop.core.models.dto.order import OrderDTO, OrderLineDTO, OrderWithDetailsDTO
from seeds_shop.infrastructure.database.models import Order, OrderLine


def convert_db_model_to_orderlines_dto(line: OrderLine) -> OrderLineDTO:
    return OrderLineDTO(product_id=line.product_id, quantity=line.quantity, final_unit_price=line.final_unit_price)


def convert_db_model_to_order_with_details_dto(
    order: Order,
    with_currency: bool = False,
    with_order_lines: bool = False,
):
    currency_symbol = ""
    if with_currency and order.payment_method:
        currency_symbol = order.payment_method.currency_symbol.value

    order_lines = []
    if with_order_lines and len(order.order_lines) > 0:
        order_lines = [convert_db_model_to_orderlines_dto(line) for line in order.order_lines]

    return OrderWithDetailsDTO(
        id=order.id,
        status=order.status,
        summ=order.summ,
        original_summ=order.original_summ,
        buyer_db_id=order.user_id,
        shop_id=order.shop_id,
        buyer_phone=order.buyer_phone,
        buyer_name=order.buyer_name,
        delivery_zone_id=order.delivery_zone_id,
        payment_method_id=order.payment_method_id,
        delivery_method_id=order.delivery_method_id,
        shipping_address=order.shipping_address,
        tracking_link=order.tracking_link,
        invoice_screenshot_path=order.invoice_screenshot_path,
        created_at=order.created_at,
        order_lines=order_lines,
        bonuses_amount=order.bonuses_amount,
        comment=order.comment,
        currency_symbol=currency_symbol,
    )


def convert_db_model_to_order_dto(order: Order) -> OrderDTO:
    return OrderDTO(
        id=order.id,
        status=order.status,
        summ=order.summ,
        original_summ=order.original_summ,
        buyer_db_id=order.user_id,
        shop_id=order.shop_id,
        buyer_name=order.buyer_name,
        buyer_phone=order.buyer_phone,
        delivery_zone_id=order.delivery_zone_id,
        payment_method_id=order.payment_method_id,
        delivery_method_id=order.delivery_method_id,
        shipping_address=order.shipping_address,
        tracking_link=order.tracking_link,
        invoice_screenshot_path=order.invoice_screenshot_path,
        bonuses_amount=order.bonuses_amount,
        comment=order.comment,
        created_at=order.created_at,
    )


def convert_cart_lines_to_order_line(cart_lines: list[CartLineDTO]) -> list[OrderLine]:
    return [
        OrderLine(product_id=item.product_id, quantity=item.quantity, final_unit_price=item.final_unit_price)
        for item in cart_lines
    ]
