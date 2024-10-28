from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CartLineDTO:
    title: str
    product_id: int
    quantity: int
    final_unit_price: Decimal | None = None


@dataclass(frozen=True)
class CartDTO:
    lines: list[CartLineDTO]
    user_id: int
    promocode: str | None = None
    bonuses_amount: int = 0
    total_amount: Decimal = Decimal(0)


@dataclass
class CartItem:
    id: int
    title: str
    price: Decimal
    quantity: int
    image_path: str | None = None
    available_quantity: int | None = None
    discounted_price: Decimal | None = None
    category_id: int | None = None


@dataclass
class WebAppCart:
    items: list[CartItem]
    promocode: str
    promocodeDiscount: int
    bonusesAmount: int
