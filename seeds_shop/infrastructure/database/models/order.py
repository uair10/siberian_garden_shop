from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import TEXT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from seeds_shop.core.models.enums.order import OrderStatus

from .base import TimedBaseModel

if TYPE_CHECKING:
    from .delivery_method import DeliveryMethod
    from .delivery_zone import DeliveryZone
    from .m2ms import OrderLine
    from .payment_details import PaymentDetails
    from .promocode import Promocode
    from .shop import Shop
    from .ticket import Ticket
    from .user import User


class Order(TimedBaseModel):
    __tablename__ = "order"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[OrderStatus] = mapped_column(server_default="created")
    order_lines: Mapped[list["OrderLine"]] = relationship(backref="order", passive_deletes="all")
    summ: Mapped[Decimal]
    original_summ: Mapped[Decimal | None]
    comment: Mapped[str | None] = mapped_column(TEXT)
    user: Mapped["User"] = relationship(back_populates="orders")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    payment_method: Mapped["PaymentDetails"] = relationship(back_populates="orders")
    payment_method_id: Mapped[int | None] = mapped_column(ForeignKey("payment_details.id"))
    delivery_method: Mapped["DeliveryMethod"] = relationship(back_populates="orders")
    delivery_method_id: Mapped[int] = mapped_column(ForeignKey("delivery_method.id"))
    shipping_address: Mapped[str | None] = mapped_column(TEXT)
    buyer_phone: Mapped[str]
    buyer_name: Mapped[str]
    shop: Mapped["Shop"] = relationship(back_populates="orders")
    shop_id: Mapped[int] = mapped_column(ForeignKey("shop.id"))
    promocode: Mapped["Promocode"] = relationship(back_populates="orders")
    promocode_id: Mapped[int | None] = mapped_column(ForeignKey("promocode.id"))
    delivery_zone: Mapped["DeliveryZone"] = relationship(back_populates="orders")
    delivery_zone_id: Mapped[int | None] = mapped_column(ForeignKey("delivery_zone.id"))
    bonuses_amount: Mapped[int | None] = mapped_column(server_default="0")
    tracking_link: Mapped[str | None]
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="order")
    invoice_screenshot_path: Mapped[str | None]

    def __repr__(self):
        return f"<Заказ №{self.id} {self.created_at}>"

    def __str__(self):
        return self.__repr__()
