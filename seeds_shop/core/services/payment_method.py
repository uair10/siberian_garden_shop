from seeds_shop.core.models.dto.payment_details import PaymentDetailsDTO
from seeds_shop.core.models.enums.currency import Currency
from seeds_shop.infrastructure.database.uow import SQLAlchemyUoW


class PaymentMethodService:
    def __init__(self, uow: SQLAlchemyUoW):
        self._uow = uow

    async def get_payment_method_by_id(self, payment_method_id: int) -> PaymentDetailsDTO:
        """Получаем метод оплаты по id"""

        return await self._uow.payment_method_reader.get_payment_method_by_id(payment_method_id)

    async def get_payment_method_by_currency(self, currency: Currency) -> PaymentDetailsDTO:
        """Получаем метод оплаты по валюте"""

        return await self._uow.payment_method_reader.get_payment_method_by_currency(currency)

    async def get_payment_methods(self) -> list[PaymentDetailsDTO]:
        """Получаем методы оплаты"""

        return await self._uow.payment_method_reader.get_payment_methods()
