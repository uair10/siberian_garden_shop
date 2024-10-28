from sqlalchemy import TEXT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TimedBaseModel


class Review(TimedBaseModel):
    __tablename__ = "review"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    review_text: Mapped[str] = mapped_column(TEXT)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="reviews")

    def __repr__(self):
        return f"<Отзыв №{self.id}>"

    def __str__(self):
        return self.__repr__()
