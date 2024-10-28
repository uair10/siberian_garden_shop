from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from seeds_shop.core.models.enums.currency import Currency, CurrencySymbol

from .base import TimedBaseModel

if TYPE_CHECKING:
    from .order import Order


class PaymentDetails(TimedBaseModel):
    __tablename__ = "payment_details"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    currency: Mapped[Currency] = mapped_column(nullable=False)
    currency_symbol: Mapped[CurrencySymbol] = mapped_column(server_default="rub")
    payment_address: Mapped[str]
    exchange_rate: Mapped[Decimal | None] = mapped_column(server_default="0")
    exchange_percent: Mapped[Decimal | None]
    payment_image_path: Mapped[str | None]
    orders: Mapped[list["Order"]] = relationship(back_populates="payment_method")

    def __repr__(self):
        return f"<{self.payment_address} {self.currency.value} {self.currency_symbol.value}>"

    def __str__(self):
        return self.__repr__()
