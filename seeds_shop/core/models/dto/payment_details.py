from dataclasses import dataclass
from decimal import Decimal

from seeds_shop.core.models.enums.currency import Currency, CurrencySymbol


@dataclass
class PaymentDetailsDTO:
    id: int
    currency: Currency
    currency_symbol: CurrencySymbol
    payment_address: str
    payment_image_path: str
    exchange_percent: Decimal | None = None
