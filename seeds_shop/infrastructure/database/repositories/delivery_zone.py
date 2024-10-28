from sqlalchemy import select

from seeds_shop.core.models.dto.delivery_zone import DeliveryZoneDTO
from seeds_shop.infrastructure.database.converters.delivery_zone import convert_db_model_to_delivery_zone_dto
from seeds_shop.infrastructure.database.exception_mapper import exception_mapper
from seeds_shop.infrastructure.database.models import DeliveryZone
from seeds_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class DeliveryZoneReaderImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_delivery_zone_by_id(self, delivery_zone: int) -> DeliveryZoneDTO:
        """Получаем зону доставки по id"""

        delivery_zone: DeliveryZone | None = await self._session.scalar(
            select(DeliveryZone)
            .where(
                DeliveryZone.id == delivery_zone,
            )
            .with_for_update(),
        )
        return convert_db_model_to_delivery_zone_dto(delivery_zone)

    @exception_mapper
    async def get_delivery_zones(self) -> list[DeliveryZoneDTO]:
        """Получаем зоны доставки"""

        res = await self._session.scalars(select(DeliveryZone))
        delivery_zones: list[DeliveryZone] = list(res)

        return [convert_db_model_to_delivery_zone_dto(zone) for zone in delivery_zones]
