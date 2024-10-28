from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import TEXT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TimedBaseModel

if TYPE_CHECKING:
    from .delivery_city import DeliveryCity
    from .order import Order


class DeliveryMethod(TimedBaseModel):
    __tablename__ = "delivery_method"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    city_id: Mapped[int] = mapped_column(ForeignKey("delivery_city.id"))
    city: Mapped["DeliveryCity"] = relationship(back_populates="delivery_methods")
    price: Mapped[Decimal]
    duration_days: Mapped[int]
    accompanying_message: Mapped[str] = mapped_column(TEXT)
    orders: Mapped[list["Order"]] = relationship(back_populates="delivery_method")

    def __repr__(self):
        return f"<Метод доставки {self.title}. Город: {self.city}. Стоимость: {self.price}>"

    def __str__(self):
        return self.__repr__()
