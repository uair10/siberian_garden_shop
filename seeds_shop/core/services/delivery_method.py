from seeds_shop.core.models.dto.delivery_method import DeliveryCityDTO, DeliveryMethodDTO
from seeds_shop.infrastructure.database.uow import SQLAlchemyUoW


class DeliveryMethodService:
    def __init__(self, uow: SQLAlchemyUoW):
        self._uow = uow

    async def get_delivery_method_by_id(self, delivery_method_id: int) -> DeliveryMethodDTO:
        return await self._uow.delivery_method_reader.get_delivery_method_by_id(delivery_method_id)

    async def get_city_by_name(self, city_name: str) -> DeliveryCityDTO | None:
        return await self._uow.delivery_method_reader.get_city_by_name(city_name)

    async def get_delivery_methods_by_city(self, city_id: int) -> list[DeliveryMethodDTO]:
        return await self._uow.delivery_method_reader.get_delivery_methods_by_city(city_id)

    async def get_delivery_cities(self, city_name: str | None = None) -> list[DeliveryCityDTO]:
        return await self._uow.delivery_method_reader.get_delivery_cities(city_name)
