from sqlalchemy import select

from seeds_shop.core.models.dto.shop import ShopDTO
from seeds_shop.infrastructure.database.converters.shop import convert_db_model_to_shop_dto
from seeds_shop.infrastructure.database.exception_mapper import exception_mapper
from seeds_shop.infrastructure.database.models import DeliveryZone, Shop
from seeds_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class ShopReaderImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_shop_by_id(self, shop_id: int) -> ShopDTO:
        shop: Shop | None = await self._session.scalar(
            select(Shop).where(
                Shop.id == shop_id,
            ),
        )

        return convert_db_model_to_shop_dto(shop)

    @exception_mapper
    async def get_shop_by_delivery_zone_id(self, delivery_zone_id: int) -> ShopDTO | None:
        """Получаем магазин по id зоны доставки"""

        shop: Shop | None = await self._session.scalar(
            select(Shop)
            .join(Shop.delivery_zones)
            .where(
                DeliveryZone.id == delivery_zone_id,
            )
        )

        if not shop:
            return None

        # TODO Рейзить ошибку если магазина нет
        return convert_db_model_to_shop_dto(shop)
