from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from seeds_shop.core.models.enums.ticket import TicketStatus

from .base import TimedBaseModel


class Ticket(TimedBaseModel):
    __tablename__ = "ticket"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[TicketStatus] = mapped_column(server_default="opened")
    admin = relationship("User", back_populates="tickets")
    admin_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"))
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str]
    order = relationship("Order", back_populates="tickets")
    order_id: Mapped[int | None] = mapped_column(ForeignKey("order.id"))

    def __repr__(self):
        return f"<Тикет от {self.telegram_id}>"

    def __str__(self):
        return self.__repr__()
