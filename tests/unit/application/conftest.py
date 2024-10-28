from decimal import Decimal

import pytest

from seeds_shop.core.models.dto.discount import DiscountDTO
from seeds_shop.core.models.dto.product import ProductDTO, ProductWithQuantityDTO


@pytest.fixture
def sample_discounts() -> list[DiscountDTO]:
    return [
        DiscountDTO(
            id=1,
            category_id=1,
            shop_id=1,
            required_quantity=3,
            discount_percent=Decimal(10),
            works_inside_category=True,
        ),
    ]


@pytest.fixture
def sample_products() -> list[ProductWithQuantityDTO]:
    return [
        ProductWithQuantityDTO(
            ProductDTO(id=1, title="Product title 1", description="Description 1", price=Decimal(120), category_id=1),
            quantity=2,
        ),
        ProductWithQuantityDTO(
            ProductDTO(id=2, title="Product title 2", description="Description 2", price=Decimal(100), category_id=1),
            quantity=1,
        ),
    ]
