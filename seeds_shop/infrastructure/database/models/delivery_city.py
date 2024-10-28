from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TimedBaseModel

if TYPE_CHECKING:
    from .delivery_method import DeliveryMethod


class DeliveryCity(TimedBaseModel):
    __tablename__ = "delivery_city"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    delivery_methods: Mapped[list["DeliveryMethod"]] = relationship(back_populates="city")

    def __repr__(self):
        return f"<Город доставки {self.title}>"

    def __str__(self):
        return self.__repr__()
