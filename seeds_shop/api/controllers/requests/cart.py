from decimal import Decimal

from pydantic import BaseModel

from seeds_shop.core.models.dto.product import ProductImageDTO


class CartItem(BaseModel):
    id: int
    title: str
    price: Decimal
    quantity: int
    images: list[ProductImageDTO] | None = None
    available_quantity: int | None = None
    discounted_price: Decimal | None = None
    category_id: int | None = None


class WebAppCart(BaseModel):
    items: list[CartItem]
    promocode: str
    promocodeDiscount: int
    bonusesAmount: int
    totalAmount: float | None = None
