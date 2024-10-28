from sqlalchemy import select

from seeds_shop.core.models.dto.payment_details import PaymentDetailsDTO
from seeds_shop.core.models.enums.currency import Currency
from seeds_shop.infrastructure.database.converters.payment_details import convert_db_model_to_payment_details_dto
from seeds_shop.infrastructure.database.exception_mapper import exception_mapper
from seeds_shop.infrastructure.database.models import PaymentDetails
from seeds_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class PaymentMethodReaderImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_payment_method_by_id(self, payment_method_id: int) -> PaymentDetailsDTO:
        """Получаем метод оплаты по id"""

        payment_method: PaymentDetails | None = await self._session.scalar(
            select(PaymentDetails).where(
                PaymentDetails.id == payment_method_id,
            ),
        )
        return convert_db_model_to_payment_details_dto(payment_method)

    @exception_mapper
    async def get_payment_method_by_currency(self, currency: Currency) -> PaymentDetailsDTO:
        """Получаем метод оплаты по валюте"""

        payment_method: PaymentDetails | None = await self._session.scalar(
            select(PaymentDetails).where(
                PaymentDetails.currency == currency,
            ),
        )

        return convert_db_model_to_payment_details_dto(payment_method)

    @exception_mapper
    async def get_payment_methods(self) -> list[PaymentDetailsDTO]:
        """
        Получаем все методы оплаты
        """

        query = select(PaymentDetails)
        res = await self._session.scalars(query)
        payment_methods: list[PaymentDetails] = list(res)

        return [convert_db_model_to_payment_details_dto(payment_method) for payment_method in payment_methods]
