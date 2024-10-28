from datetime import timedelta

from sqlalchemy import and_, desc, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm import joinedload

from seeds_shop.core.exceptions.common import RepoError
from seeds_shop.core.exceptions.order import OrderIdAlreadyExist
from seeds_shop.core.models.dto.order import OrderDTO, OrderWithDetailsDTO
from seeds_shop.core.models.enums.order import OrderStatus
from seeds_shop.core.utils.date_time import get_date_time
from seeds_shop.infrastructure.database.converters.order import (
    convert_db_model_to_order_dto,
    convert_db_model_to_order_with_details_dto,
)
from seeds_shop.infrastructure.database.exception_mapper import exception_mapper
from seeds_shop.infrastructure.database.models import Order, User
from seeds_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class OrderReaderImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_order_by_id(self, order_id: int) -> OrderWithDetailsDTO | None:
        """Получаем заказ по id"""

        query = (
            select(Order)
            .where(Order.id == order_id)
            .options(joinedload(Order.order_lines), joinedload(Order.payment_method))
        )
        order: Order | None = await self._session.scalar(query)

        if not order:
            return None

        return convert_db_model_to_order_with_details_dto(order, True, True)

    @exception_mapper
    async def get_user_orders(self, user_tg_id: int) -> list[OrderWithDetailsDTO]:
        """Получаем заказы пользователя"""

        query = (
            select(Order)
            .outerjoin(Order.user)
            .where(User.telegram_id == user_tg_id)
            .options(joinedload(Order.payment_method))
            .order_by(desc(Order.created_at))
        )

        res = await self._session.scalars(query)
        orders: list[Order] = list(res.unique())

        return [convert_db_model_to_order_with_details_dto(order, True) for order in orders]

    @exception_mapper
    async def get_orders_for_confirmation(self) -> list[OrderWithDetailsDTO]:
        query = (
            select(Order)
            .where(
                and_(Order.status == OrderStatus.payment_not_confirmed),
                Order.invoice_screenshot_path != None,  # noqa: E711
            )
            .order_by(desc(Order.created_at))
            .options(joinedload(Order.payment_method))
        )

        res = await self._session.scalars(query)
        orders: list[Order] = list(res.unique())

        return [convert_db_model_to_order_with_details_dto(order, True) for order in orders]

    @exception_mapper
    async def get_orders_for_shipping(self) -> list[OrderWithDetailsDTO]:
        """Получаем заказы для отгрузки"""

        query = (
            select(Order)
            .where(
                and_(
                    Order.status == OrderStatus.payment_confirmed,
                    Order.tracking_link == None,  # noqa: E711
                ),
            )
            .order_by(desc(Order.created_at))
            .options(joinedload(Order.payment_method))
        )

        res = await self._session.scalars(query)
        orders: list[Order] = list(res.unique())

        return [convert_db_model_to_order_with_details_dto(order, True) for order in orders]

    @exception_mapper
    async def get_expired_payment_orders(self) -> list[OrderWithDetailsDTO]:
        """Получаем заказы с более чем часом в статусе payment_canceled"""

        date_now = get_date_time()

        query = (
            select(Order)
            .where(
                and_(
                    Order.status == OrderStatus.payment_canceled,
                    Order.updated_at <= date_now - timedelta(hours=1),
                ),
            )
            .options(joinedload(Order.order_lines))
        )

        res = await self._session.scalars(query)
        orders: list[Order] = list(res.unique())

        return [convert_db_model_to_order_with_details_dto(order, with_order_lines=True) for order in orders]

    @exception_mapper
    async def get_completed_orders(self) -> list[OrderDTO]:
        """Получаем заказы с более чем 3 часами в статусе in_transit"""

        date_now = get_date_time()

        query = select(Order).where(
            and_(
                Order.status == OrderStatus.payment_canceled,
                Order.updated_at <= date_now - timedelta(hours=3),
            ),
        )

        res = await self._session.scalars(query)
        orders: list[Order] = list(res)

        return [convert_db_model_to_order_dto(order) for order in orders]

    @exception_mapper
    async def get_order_with_promocode(self, user_tg_id: int, promocode_id: int) -> OrderDTO | None:
        query = (
            select(Order)
            .outerjoin(Order.user)
            .where(and_(User.telegram_id == user_tg_id, Order.promocode_id == promocode_id))
        )

        order: Order | None = await self._session.scalar(query)

        if not order:
            return None

        return convert_db_model_to_order_dto(order)


class OrderRepoImpl(SQLAlchemyRepo):
    @exception_mapper
    async def acquire_order_by_id(self, order_id: int) -> Order | None:
        """Получаем заказ по id"""

        query = (
            select(Order)
            .where(Order.id == order_id)
            .options(joinedload(Order.order_lines), joinedload(Order.payment_method))
        )
        order: Order | None = await self._session.scalar(query)

        if not order:
            return None

        return order

    @exception_mapper
    async def create_order(self, order: Order):
        self._session.add(order)
        try:
            await self._session.flush((order,))
        except IntegrityError as err:
            self._parse_error(err)

    @exception_mapper
    async def update_order(self, order: Order) -> None:
        try:
            await self._session.merge(order)
        except IntegrityError as err:
            self._parse_error(err)

    @staticmethod
    def _parse_error(err: DBAPIError) -> None:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "pk_order":
                raise OrderIdAlreadyExist from err
            case _:
                raise RepoError from err
