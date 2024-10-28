from seeds_shop.core.models.dto.delivery_zone import DeliveryZoneDTO
from seeds_shop.infrastructure.database.models import DeliveryZone


def convert_db_model_to_delivery_zone_dto(
    delivery_zone: DeliveryZone,
) -> DeliveryZoneDTO:
    return DeliveryZoneDTO(
        id=delivery_zone.id,
        title=delivery_zone.title,
    )
