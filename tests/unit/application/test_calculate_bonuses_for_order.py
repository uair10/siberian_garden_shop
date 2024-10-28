from decimal import Decimal

from seeds_shop.core.price_calculation import calculate_bonuses_for_order


def test_calculate_bonuses_for_order():
    order_summ = Decimal(1200)
    bonuses_for_order = calculate_bonuses_for_order(order_summ, 10)

    assert bonuses_for_order == 120
