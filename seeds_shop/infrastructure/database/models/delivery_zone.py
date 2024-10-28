from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TimedBaseModel
from .m2ms import delivery_zones_shops

if TYPE_CHECKING:
    from .order import Order
    from .shop import Shop
    from .stock import Stock
    from .user import User


class DeliveryZone(TimedBaseModel):
    __tablename__ = "delivery_zone"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    users: Mapped[list["User"]] = relationship(foreign_keys="User.delivery_zone_id", back_populates="delivery_zone")
    admin_users: Mapped[list["User"]] = relationship(
        foreign_keys="User.working_delivery_zone_id",
        back_populates="working_delivery_zone",
    )
    shops: Mapped[list["Shop"]] = relationship(
        secondary=delivery_zones_shops, back_populates="delivery_zones", cascade="all,delete"
    )
    orders: Mapped[list["Order"]] = relationship(back_populates="delivery_zone")
    stocks: Mapped[list["Stock"]] = relationship(back_populates="delivery_zone", cascade="all,delete")

    def __repr__(self):
        return f"<Зона доставки {self.title}>"

    def __str__(self):
        return self.__repr__()
