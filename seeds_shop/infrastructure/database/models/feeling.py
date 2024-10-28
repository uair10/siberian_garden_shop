from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TimedBaseModel
from .m2ms import products_feelings


class Feeling(TimedBaseModel):
    __tablename__ = "feeling"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    products = relationship("Product", secondary=products_feelings, back_populates="feelings")

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.__repr__()
