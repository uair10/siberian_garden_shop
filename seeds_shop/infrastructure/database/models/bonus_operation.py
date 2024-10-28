from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from seeds_shop.core.models.enums.bonus import OperationType

from .base import TimedBaseModel


class BonusOperation(TimedBaseModel):
    __tablename__ = "bonus_operation"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    user = relationship("User", back_populates="bonuses_operations")
    user_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"))
    operation_type: Mapped[OperationType]
    amount: Mapped[int]

    def __repr__(self):
        return f"<Бонус №{self.id}>"

    def __str__(self):
        return self.__repr__()
