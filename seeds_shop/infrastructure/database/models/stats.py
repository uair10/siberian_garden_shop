import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from .base import TimedBaseModel


class Statistics(TimedBaseModel):
    __tablename__ = "stats"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.datetime] = mapped_column(unique=True, server_default=func.now())
    products_purchased: Mapped[int] = mapped_column(server_default="0")
    orders_created: Mapped[int] = mapped_column(server_default="0")
    users_registered: Mapped[int] = mapped_column(server_default="0")
    tickets_opened: Mapped[int] = mapped_column(server_default="0")

    def __repr__(self):
        return f"<Статистика №{self.id} за день {self.date}>"
