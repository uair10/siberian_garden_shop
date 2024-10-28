from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from seeds_shop.infrastructure.database.models.base import TimedBaseModel

products_feelings = Table(
    "product_feelings",
    TimedBaseModel.metadata,
    Column("product_id", Integer, ForeignKey("product.id")),
    Column("feeling_id", Integer, ForeignKey("feeling.id")),
)

products_genetics = Table(
    "products_genetics",
    TimedBaseModel.metadata,
    Column("product_id", Integer, ForeignKey("product.id")),
    Column("genetics_id", Integer, ForeignKey("genetics.id")),
)

promocodes_users = Table(
    "promocodes_users",
    TimedBaseModel.metadata,
    Column("promocode_id", Integer, ForeignKey("promocode.id")),
    Column("user_id", Integer, ForeignKey("user.id")),
)


delivery_zones_shops = Table(
    "delivery_zones_shops",
    TimedBaseModel.metadata,
    Column("delivery_zone_id", Integer, ForeignKey("delivery_zone.id")),
    Column("shop_id", Integer, ForeignKey("shop.id")),
)


class OrderLine(TimedBaseModel):
    __tablename__ = "order_line"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id", ondelete="CASCADE"))
    product = relationship("Product", backref=backref("order_lines", cascade="all,delete"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    quantity: Mapped[int]
    final_unit_price: Mapped[float]

    def __repr__(self):
        return f"<Заказ №{self.id}, товар №{self.product_id}, количество: {self.quantity}, итоговая цена: {self.final_unit_price}>"

    def __str__(self):
        return self.__repr__()
