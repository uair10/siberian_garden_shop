import logging
from decimal import Decimal

from seeds_shop.core.exceptions.bonus import InsufficientBonuses
from seeds_shop.core.exceptions.order import InsufficientStock
from seeds_shop.core.models.dto.bot_settings import BotSettingsDTO
from seeds_shop.core.models.dto.order import OrderDTO, OrderWithDetailsDTO
from seeds_shop.core.models.enums.bonus import OperationType
from seeds_shop.core.models.enums.order import OrderStatus
from seeds_shop.infrastructure.database.converters.order import convert_db_model_to_order_with_details_dto
from seeds_shop.infrastructure.database.models import BonusOperation, Order, OrderLine, Stock
from seeds_shop.infrastructure.database.uow import SQLAlchemyUoW

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self, uow: SQLAlchemyUoW):
        self._uow = uow

    async def get_order_by_id(self, order_id: int) -> OrderWithDetailsDTO:
        """Получаем заказ по id"""

        return await self._uow.order_reader.get_order_by_id(order_id)

    async def get_user_orders(self, user_tg_id: int) -> list[OrderWithDetailsDTO]:
        """Получаем заказы пользователя"""

        return await self._uow.order_reader.get_user_orders(user_tg_id)

    async def get_orders_for_confirmation(self) -> list[OrderWithDetailsDTO]:
        """Получаем заказы с неподтвержденной оплатой"""

        return await self._uow.order_reader.get_orders_for_confirmation()

    async def get_orders_for_shipping(self) -> list[OrderWithDetailsDTO]:
        """Получаем заказы для отгрузки"""

        return await self._uow.order_reader.get_orders_for_shipping()

    async def get_expired_payment_orders(self) -> list[OrderWithDetailsDTO]:
        """Получаем заказы с более чем часом в статусе payment_canceled"""

        return await self._uow.order_reader.get_expired_payment_orders()

    async def get_completed_orders(self) -> list[OrderDTO]:
        """Получаем заказы с более чем 3 часами в статусе in transit"""

        return await self._uow.order_reader.get_completed_orders()

    async def get_order_with_promocode(self, user_id: int, promocode_id: int) -> OrderDTO:
        """Получаем заказ с промокодом"""

        return await self._uow.order_reader.get_order_with_promocode(user_id, promocode_id)

    async def create_order(
        self,
        summ: Decimal,
        original_summ: Decimal,
        user_id: int,
        shop_id: int,
        buyer_phone: str,
        buyer_name: str,
        delivery_address: str,
        delivery_zone_id: int,
        payment_method_id: int,
        delivery_method_id: int,
        order_lines: list[OrderLine],
        comment: str | None = None,
        promocode_id: int | None = None,
        bonuses_amount: int | None = None,
        order_status: OrderStatus = OrderStatus.created,
    ) -> OrderWithDetailsDTO:
        """
        Создаем заказ
        :param summ: Сумма заказа
        :param original_summ: Сумма заказа до конвертации валюты
        :param user_id: Id пользователя
        :param shop_id: Id магазина
        :param buyer_phone: Адрес делефона заказчика
        :param buyer_name: Имя заказчика
        :param delivery_address: Адрес доставки
        :param delivery_zone_id: Зона доставки
        :param payment_method_id: Id метода оплаты
        :param delivery_method_id: Метод доставки заказа
        :param order_lines: Список купленных товаров
        :param comment: Комментарий
        :param promocode_id: Id промокода
        :param bonuses_amount: Кол-во бонусов
        :param order_status: Статус заказа
        """
        # TODO Вынести весь этот функционал в use cases

        bot_settings: BotSettingsDTO = await self._uow.bot_settings_reader.get_bot_settings()
        users_bonuses: int = await self._uow.bonus_reader.get_user_bonus_balance(
            user_id,
            bot_settings.days_before_using_bonus,
        )
        if bonuses_amount and users_bonuses < bonuses_amount:
            raise InsufficientBonuses

        order = Order(
            summ=summ,
            original_summ=original_summ,
            status=order_status,
            order_lines=order_lines,
            user_id=user_id,
            delivery_method_id=delivery_method_id,
            shipping_address=delivery_address,
            buyer_phone=buyer_phone,
            buyer_name=buyer_name,
            shop_id=shop_id,
            delivery_zone_id=delivery_zone_id,
            payment_method_id=payment_method_id,
            comment=comment,
            promocode_id=promocode_id,
            bonuses_amount=bonuses_amount,
        )
        # Уменьшаем остатки по товару в магазине
        for line in order_lines:
            stock: Stock = await self._uow.product_repo.acquire_product_stock_in_shop(
                shop_id, delivery_zone_id, line.product_id
            )
            if stock.available_quantity < line.quantity:
                raise InsufficientStock(
                    product_id=line.product_id,
                    requested_amount=line.quantity,
                    available_amount=stock.available_quantity,
                )
            stock.available_quantity -= line.quantity
            await self._uow.product_repo.update_stock(stock)
        try:
            await self._uow.order_repo.create_order(order)
            if bonuses_amount and bonuses_amount > 0:
                bonus_operation = BonusOperation(
                    user_id=user_id,
                    operation_type=OperationType.DEDUCTION,
                    amount=bonuses_amount,
                )
                await self._uow.bonus_repo.create_bonus_operation(bonus_operation)
        except Exception as err:
            await self._uow.rollback()
            raise err

        await self._uow.commit()

        logger.info(f"Order was created: {order.id}")

        return convert_db_model_to_order_with_details_dto(order, False, True)

    async def update_order_status(self, order_id: int, order_status: OrderStatus) -> None:
        """Обновляем статус заказа"""

        order: Order = await self._uow.order_repo.acquire_order_by_id(order_id)
        order.status = order_status
        await self._uow.order_repo.update_order(order)

        await self._uow.commit()

        logger.info(f"Order {order_id} status was updated. New status: {order_status}")

    async def update_order_summ(self, order_id: int, summ: Decimal) -> None:
        """Обновляем сумму заказа"""

        order: Order = await self._uow.order_repo.acquire_order_by_id(order_id)
        order.summ = summ
        await self._uow.order_repo.update_order(order)

        await self._uow.commit()

        logger.info(f"Order {order_id} summ was updated. New summ: {summ}")

    async def update_order_invoice_path(self, order_id: int, invoice_filename: str) -> None:
        """Обновляем путь к скриншоту об оплате"""

        order: Order = await self._uow.order_repo.acquire_order_by_id(order_id)
        order.status = OrderStatus.payment_not_confirmed
        order.invoice_screenshot_path = invoice_filename

        await self._uow.order_repo.update_order(order)

        await self._uow.commit()

        logger.info(f"Order {order_id} invoice screenshot path was updated")

    async def update_order_payment_method(self, order_id: int, payment_method_id: int) -> None:
        """Обновляем способ оплаты заказа"""

        order: Order = await self._uow.order_repo.acquire_order_by_id(order_id)
        order.payment_method_id = payment_method_id
        order.status = OrderStatus.created

        await self._uow.order_repo.update_order(order)

        await self._uow.commit()

        logger.info(f"Order {order_id} payment method was updated")

    async def update_order_tracking_link(self, order_id: int, tracking_link: str) -> None:
        """Обновляем ссылку на отслеживание заказа"""

        order: Order = await self._uow.order_repo.acquire_order_by_id(order_id)
        order.tracking_link = tracking_link
        order.status = OrderStatus.in_transit

        await self._uow.order_repo.update_order(order)

        await self._uow.commit()

        logger.info(f"Order {order_id} tracking link was updated")
