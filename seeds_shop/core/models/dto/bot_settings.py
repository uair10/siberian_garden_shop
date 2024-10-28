import datetime
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class BotSettingsDTO:
    is_bot_enabled: bool
    days_before_using_bonus: int
    maximum_bonus_for_order_percent: float
    maximum_bonus_discount_percent: float
    paid_delivery_enabled: bool
    free_delivery_threshold: Decimal
    bot_disabled_until: datetime.datetime | None = None
