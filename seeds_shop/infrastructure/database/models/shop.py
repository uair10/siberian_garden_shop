from sqlalchemy import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TimedBaseModel
from .m2ms import delivery_zones_shops


class Shop(TimedBaseModel):
    __tablename__ = "shop"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    stock = relationship("Stock", back_populates="shop", cascade="all,delete")
    orders = relationship("Order", back_populates="shop", cascade="all,delete")
    discounts = relationship("Discount", back_populates="shop")
    workers = relationship("User", back_populates="shop")
    delivery_zones = relationship("DeliveryZone", secondary=delivery_zones_shops, back_populates="shops")
    contact_address: Mapped[str] = mapped_column(TEXT)

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.__repr__()
