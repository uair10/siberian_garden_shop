from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TimedBaseModel
from .m2ms import products_genetics


class Genetics(TimedBaseModel):
    __tablename__ = "genetics"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    products = relationship("Product", secondary=products_genetics, back_populates="genetics")

    def __repr__(self):
        return f"<Genetic {self.title}>"

    def __str__(self):
        return self.__repr__()
