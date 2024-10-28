from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TimedBaseModel


class Stock(TimedBaseModel):
    __tablename__ = "stock"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    product = relationship("Product", back_populates="stock")
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    shop = relationship("Shop", back_populates="stock")
    shop_id: Mapped[int] = mapped_column(ForeignKey("shop.id"))
    available_quantity: Mapped[int]
    delivery_zone = relationship("DeliveryZone", back_populates="stocks")
    delivery_zone_id: Mapped[int | None] = mapped_column(ForeignKey("delivery_zone.id"))

    def __repr__(self):
        return f"<{self.product.title} в магазине {self.shop.title}: {self.available_quantity} шт."

    def __str__(self):
        return self.__repr__()
