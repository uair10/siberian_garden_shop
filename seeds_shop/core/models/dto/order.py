import datetime
from dataclasses import dataclass
from decimal import Decimal

from seeds_shop.core.models.enums.order import OrderStatus


@dataclass(frozen=True)
class OrderLineDTO:
    product_id: int
    quantity: int
    final_unit_price: Decimal


@dataclass(frozen=True)
class OrderDTO:
    id: int
    status: OrderStatus
    summ: Decimal
    buyer_db_id: int
    shop_id: int
    delivery_zone_id: int
    payment_method_id: int
    delivery_method_id: int
    buyer_phone: str
    buyer_name: str
    created_at: datetime.datetime
    original_summ: Decimal | None = None
    promocode_id: int | None = None
    shipping_address: str | None = None
    tracking_link: str | None = None
    bonuses_amount: int | None = None
    comment: str | None = None
    invoice_screenshot_path: str | None = None


@dataclass(frozen=True)
class OrderWithDetailsDTO(OrderDTO):
    order_lines: list[OrderLineDTO] | None = None
    currency_symbol: str | None = None
