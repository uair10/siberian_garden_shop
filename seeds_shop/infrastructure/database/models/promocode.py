from sqlalchemy.orm import Mapped, mapped_column, relationship

from seeds_shop.core.models.enums.promocode import PromocodeStatus
from seeds_shop.infrastructure.database.models.base import TimedBaseModel
from seeds_shop.infrastructure.database.models.m2ms import promocodes_users


class Promocode(TimedBaseModel):
    __tablename__ = "promocode"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[PromocodeStatus] = mapped_column(
        server_default="active",
    )
    users = relationship("User", secondary=promocodes_users, back_populates="promocodes")
    orders = relationship("Order", back_populates="promocode")
    limit: Mapped[int] = mapped_column(server_default="0")
    reusable: Mapped[bool] = mapped_column(server_default="0")
    uses_number: Mapped[int] = mapped_column(server_default="0")

    def __repr__(self):
        return f"<Промокод №{self.id} {self.name}>"

    def __str__(self):
        return self.__repr__()
