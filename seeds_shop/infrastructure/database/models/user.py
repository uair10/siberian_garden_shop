from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from seeds_shop.core.models.enums.user import LangCode, UserRole

from .base import TimedBaseModel
from .m2ms import promocodes_users


class User(TimedBaseModel):
    __tablename__ = "user"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str]
    role: Mapped[UserRole] = mapped_column(server_default="user")
    orders = relationship("Order", back_populates="user", cascade="all,delete")
    bonuses_operations = relationship("BonusOperation", back_populates="user", cascade="all,delete")
    delivery_zone_id: Mapped[int | None] = mapped_column(ForeignKey("delivery_zone.id"))
    delivery_zone = relationship("DeliveryZone", foreign_keys=delivery_zone_id, back_populates="users")
    working_delivery_zone_id: Mapped[int | None] = mapped_column(
        ForeignKey("delivery_zone.id"),
    )
    working_delivery_zone = relationship(
        "DeliveryZone",
        foreign_keys=working_delivery_zone_id,
        back_populates="admin_users",
    )
    shop = relationship("Shop", back_populates="workers")
    shop_id: Mapped[int | None] = mapped_column(ForeignKey("shop.id"))
    reviews = relationship("Review", back_populates="user", cascade="all,delete")
    lang_code: Mapped[LangCode] = mapped_column(server_default="en")
    tickets = relationship("Ticket", back_populates="admin", cascade="all,delete")
    promocodes = relationship(
        "Promocode",
        secondary=promocodes_users,
        back_populates="users",
    )

    def __repr__(self):
        return f"<Пользователь №{self.id} {self.telegram_id}>"

    def __str__(self):
        return self.__repr__()
