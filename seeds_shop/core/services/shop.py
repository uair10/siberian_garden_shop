from seeds_shop.core.models.dto.shop import ShopDTO
from seeds_shop.infrastructure.database.uow import SQLAlchemyUoW


class ShopService:
    def __init__(self, uow: SQLAlchemyUoW):
        self._uow = uow

    async def get_shop_by_id(self, shop_id: int) -> ShopDTO | None:
        return await self._uow.shop_reader.get_shop_by_id(shop_id)

    async def get_shop_by_delivery_zone_id(self, delivery_zone_id: int) -> ShopDTO | None:
        """Получаем магазин по id зоны доставки"""

        return await self._uow.shop_reader.get_shop_by_delivery_zone_id(delivery_zone_id)
