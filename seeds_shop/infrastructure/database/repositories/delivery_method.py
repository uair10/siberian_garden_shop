from sqlalchemy import select

from seeds_shop.core.models.dto.delivery_method import DeliveryCityDTO, DeliveryMethodDTO
from seeds_shop.infrastructure.database.converters.delivery_method import (
    convert_db_model_to_delivery_city_dto,
    convert_db_model_to_delivery_method_dto,
)
from seeds_shop.infrastructure.database.exception_mapper import exception_mapper
from seeds_shop.infrastructure.database.models import DeliveryCity, DeliveryMethod, PaymentDetails
from seeds_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class DeliveryMethodReaderImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_delivery_method_by_id(self, delivery_method_id: int) -> DeliveryMethodDTO:
        delivery_method: DeliveryMethod | None = await self._session.scalar(
            select(DeliveryMethod).where(
                PaymentDetails.id == delivery_method_id,
            ),
        )
        return convert_db_model_to_delivery_method_dto(delivery_method)

    @exception_mapper
    async def get_city_by_name(self, city_name: str) -> DeliveryCityDTO | None:
        city: DeliveryCity | None = await self._session.scalar(
            select(DeliveryCity).where(DeliveryCity.title.ilike(city_name))
        )

        if not city:
            return None

        return convert_db_model_to_delivery_city_dto(city)

    @exception_mapper
    async def get_delivery_methods_by_city(self, city_id: int) -> list[DeliveryMethodDTO]:
        query = select(DeliveryMethod).where(DeliveryMethod.city_id == city_id)

        res = await self._session.scalars(query)
        delivery_methods: list[DeliveryMethod] = list(res)

        return [convert_db_model_to_delivery_method_dto(delivery_method) for delivery_method in delivery_methods]

    @exception_mapper
    async def get_delivery_cities(self, city_name: str | None = None) -> list[DeliveryCityDTO]:
        query = select(DeliveryCity)

        if city_name is not None:
            query = query.where(DeliveryCity.title.ilike(city_name))

        res = await self._session.scalars(query)
        cities: list[DeliveryCity] = list(res)

        return [convert_db_model_to_delivery_city_dto(city) for city in cities]
