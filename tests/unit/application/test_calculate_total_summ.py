from decimal import Decimal

from seeds_shop.core.models.dto.discount import DiscountDTO
from seeds_shop.core.models.dto.product import ProductDTO, ProductWithQuantityDTO
from seeds_shop.core.models.enums.currency import Currency
from seeds_shop.core.price_calculation import calculate_delivery_cost, calculate_total_summ


def test_calculate_total_summ(sample_products: list[ProductWithQuantityDTO], sample_discounts: list[DiscountDTO]):
    total_summ = calculate_total_summ(
        sample_products,
        maximum_bonus_discount_percent=20,
        discounts=sample_discounts,
        currency=Currency.rub,
        paid_delivery_enabled=False,
        delivery_price=Decimal(100),
        free_delivery_threshold=Decimal(120),
    )
    assert total_summ == Decimal("306")


def test_calculate_total_summ_with_promocode(
    sample_products: list[ProductWithQuantityDTO],
    sample_discounts: list[DiscountDTO],
):
    total_summ = calculate_total_summ(
        sample_products,
        maximum_bonus_discount_percent=20,
        discounts=sample_discounts,
        currency=Currency.rub,
        promocode_percent=Decimal(10),
        paid_delivery_enabled=False,
        delivery_price=Decimal(100),
        free_delivery_threshold=Decimal(120),
    )
    assert total_summ == Decimal("275.40")


def test_calculate_total_summ_with_bonuses(
    sample_products: list[ProductWithQuantityDTO],
    sample_discounts: list[DiscountDTO],
):
    total_summ = calculate_total_summ(
        sample_products,
        maximum_bonus_discount_percent=20,
        discounts=sample_discounts,
        currency=Currency.rub,
        bonuses_amount=50,
        paid_delivery_enabled=False,
        delivery_price=Decimal(100),
        free_delivery_threshold=Decimal(120),
    )
    assert total_summ == Decimal("256.00")


def test_calculate_total_summ_with_exchange(
    sample_products: list[ProductWithQuantityDTO],
    sample_discounts: list[DiscountDTO],
):
    total_summ = calculate_total_summ(
        sample_products,
        maximum_bonus_discount_percent=20,
        discounts=sample_discounts,
        currency=Currency.ton,
        exchange_rate=Decimal(78.56),
        exchange_percent=Decimal(2),
        paid_delivery_enabled=False,
        delivery_price=Decimal(100),
        free_delivery_threshold=Decimal(120),
    )
    assert total_summ == Decimal("3.96")


def test_calculate_total_summ_with_btc_currency(
    sample_products: list[ProductWithQuantityDTO],
    sample_discounts: list[DiscountDTO],
):
    total_summ = calculate_total_summ(
        sample_products,
        maximum_bonus_discount_percent=20,
        discounts=sample_discounts,
        currency=Currency.btc,
        exchange_rate=Decimal(50000),
        paid_delivery_enabled=False,
        delivery_price=Decimal(100),
        free_delivery_threshold=Decimal(120),
    )
    assert total_summ == Decimal("0.00612000")


def test_calculate_total_summ_with_paid_delivery(
    sample_products: list[ProductWithQuantityDTO], sample_discounts: list[DiscountDTO]
):
    paid_delivery_enabled = True
    delivery_price = Decimal(100)
    free_delivery_threshold = Decimal(500)
    total_summ = calculate_total_summ(
        sample_products,
        maximum_bonus_discount_percent=20,
        discounts=sample_discounts,
        currency=Currency.rub,
        paid_delivery_enabled=paid_delivery_enabled,
        delivery_price=delivery_price,
        free_delivery_threshold=Decimal(500),
    )
    delivery_cost = calculate_delivery_cost(
        paid_delivery_enabled=True,
        delivery_price=delivery_price,
        order_summ=total_summ,
        free_delivery_threshold=free_delivery_threshold,
    )
    assert delivery_cost == delivery_price
    assert total_summ == Decimal("406")


def test_calculate_total_summ_with_free_delivery(
    sample_products: list[ProductWithQuantityDTO], sample_discounts: list[DiscountDTO]
):
    paid_delivery_enabled = True
    delivery_price = Decimal(100)
    free_delivery_threshold = Decimal(500)
    sample_products.append(
        ProductWithQuantityDTO(
            ProductDTO(id=3, title="Product title 3", description="Description 3", price=Decimal(200), category_id=1),
            quantity=1,
        )
    )
    total_summ = calculate_total_summ(
        sample_products,
        maximum_bonus_discount_percent=20,
        discounts=sample_discounts,
        currency=Currency.rub,
        paid_delivery_enabled=paid_delivery_enabled,
        delivery_price=delivery_price,
        free_delivery_threshold=free_delivery_threshold,
    )
    delivery_cost = calculate_delivery_cost(
        paid_delivery_enabled=True,
        delivery_price=delivery_price,
        order_summ=total_summ,
        free_delivery_threshold=free_delivery_threshold,
    )
    assert delivery_cost == Decimal(0)
    assert total_summ == Decimal("586")
