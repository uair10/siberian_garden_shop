from sqlalchemy import False_, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TimedBaseModel


class Discount(TimedBaseModel):
    __tablename__ = "discount"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    shop = relationship("Shop", back_populates="discounts")
    shop_id: Mapped[int | None] = mapped_column(ForeignKey("shop.id"))
    category = relationship("Category", back_populates="discounts")
    category_id: Mapped[int | None] = mapped_column(ForeignKey("category.id"))
    discount_percent: Mapped[float]
    required_quantity: Mapped[int]
    works_inside_category: Mapped[bool] = mapped_column(server_default=False_())

    def __repr__(self):
        return f"<Скидка №{self.id}>"

    def __str__(self):
        return self.__repr__()
