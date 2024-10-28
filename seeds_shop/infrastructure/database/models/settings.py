import datetime
from decimal import Decimal

from sqlalchemy import True_
from sqlalchemy.orm import Mapped, mapped_column

from .base import TimedBaseModel


class BotSettings(TimedBaseModel):
    __tablename__ = "bot_settings"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    is_bot_enabled: Mapped[bool] = mapped_column(server_default=True_())
    days_before_using_bonus: Mapped[int] = mapped_column(server_default="0")
    maximum_bonus_for_order_percent: Mapped[int] = mapped_column(server_default="0")
    maximum_bonus_discount_percent: Mapped[int] = mapped_column(server_default="0")
    bot_disabled_until: Mapped[datetime.datetime | None]
    paid_delivery_enabled: Mapped[bool] = mapped_column(server_default=True_())
    free_delivery_threshold: Mapped[Decimal]
