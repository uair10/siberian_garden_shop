from decimal import Decimal

from seeds_shop.core.models.enums.product import MeasurementUnit


def format_product_line(
    product_title: str,
    product_total: Decimal,
    measurement: MeasurementUnit,
    quantity: int,
    currency_symbol: str = "₽",
):
    """Форматируем строку товара"""

    measurement_unit = "gr."
    if measurement == MeasurementUnit.pcs:
        measurement_unit = "pcs."
    return f"- {product_title} ({quantity} {measurement_unit}) – {product_total} {currency_symbol}\n"
