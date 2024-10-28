from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TimedBaseModel


class Category(TimedBaseModel):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    products = relationship("Product", back_populates="category")
    discounts = relationship("Discount", back_populates="category")
    position_number: Mapped[int] = mapped_column(server_default="0")

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Категория №{self.id} {self.title}>"
