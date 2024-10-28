from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class DiscountDTO:
    id: int
    shop_id: int
    category_id: int
    required_quantity: int
    discount_percent: Decimal
    works_inside_category: bool
