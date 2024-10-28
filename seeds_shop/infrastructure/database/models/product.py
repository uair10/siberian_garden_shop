from sqlalchemy import TEXT, False_, ForeignKey, True_
from sqlalchemy.orm import Mapped, mapped_column, relationship

from seeds_shop.core.models.enums.product import MeasurementUnit, StrainType

from .base import TimedBaseModel
from .m2ms import products_feelings, products_genetics


class ProductImage(TimedBaseModel):
    __tablename__ = "product_image"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    image_path: Mapped[str]
    product = relationship("Product", back_populates="images")


class Product(TimedBaseModel):
    __tablename__ = "product"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    images = relationship("ProductImage", back_populates="product", cascade="all,delete")
    description: Mapped[str] = mapped_column(TEXT)
    measurement: Mapped[MeasurementUnit] = mapped_column(server_default="grams")
    stock = relationship("Stock", back_populates="product", cascade="all,delete")
    category = relationship("Category", back_populates="products")
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    price: Mapped[float]
    weight: Mapped[float] = mapped_column(server_default="1")
    sold_count: Mapped[int] = mapped_column(server_default="0")
    feelings = relationship("Feeling", secondary=products_feelings, back_populates="products")
    genetics = relationship("Genetics", secondary=products_genetics, back_populates="products")
    strain_name: Mapped[str | None]
    strain_type: Mapped[StrainType | None]
    thc: Mapped[int | None]
    origin: Mapped[str | None]
    pgr: Mapped[bool] = mapped_column(server_default=False_())
    vhq: Mapped[bool] = mapped_column(server_default=True_())
    cbd: Mapped[str | None]
    webapp_position: Mapped[int] = mapped_column(server_default="0")
    sku: Mapped[str | None] = mapped_column(unique=True)

    def __repr__(self):
        return f"<Товар №{self.id} {self.title}>"

    def __str__(self):
        return self.__repr__()
