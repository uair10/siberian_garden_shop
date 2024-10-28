from decimal import Decimal

from seeds_shop.core.models.dto.discount import DiscountDTO
from seeds_shop.core.models.dto.product import ProductWithQuantityDTO
from seeds_shop.core.models.enums.currency import Currency
from seeds_shop.core.price_calculation import calculate_product_discounted_price


def test_calculate_product_discounted_price_no_discount(sample_products: list[ProductWithQuantityDTO]):
    product = sample_products[0].product
    discounted_price = calculate_product_discounted_price(
        product,
        2,
        sample_products,
        maximum_bonus_discount_percent=20,
        discounts=[],
    )
    assert discounted_price == Decimal("120")


def test_calculate_product_discounted_price_with_discount(
    sample_products: list[ProductWithQuantityDTO],
    sample_discounts: list[DiscountDTO],
):
    product = sample_products[0].product
    discounted_price = calculate_product_discounted_price(
        product,
        1,
        sample_products,
        maximum_bonus_discount_percent=20,
        discounts=sample_discounts,
        currency=Currency.rub,
    )
    assert discounted_price == Decimal("108")
