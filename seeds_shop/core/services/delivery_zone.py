from seeds_shop.core.models.dto.delivery_zone import DeliveryZoneDTO
from seeds_shop.infrastructure.database.uow import SQLAlchemyUoW


class DeliveryZoneService:
    """Сервис для работы с зонами доставки"""

    def __init__(self, uow: SQLAlchemyUoW):
        self._uow = uow

    async def get_delivery_zone_by_id(self, delivery_zone_id: int) -> DeliveryZoneDTO:
        """Получаем пользователя по id"""

        return await self._uow.delivery_zone_reader.get_delivery_zone_by_id(delivery_zone_id)

    async def get_all_delivery_zones(self) -> list[DeliveryZoneDTO]:
        """Получаем все зоны доставки"""

        return await self._uow.delivery_zone_reader.get_delivery_zones()
