from seeds_shop.core.models.dto.delivery_method import DeliveryCityDTO, DeliveryMethodDTO
from seeds_shop.infrastructure.database.models import DeliveryCity, DeliveryMethod


def convert_db_model_to_delivery_city_dto(
    delivery_city: DeliveryCity,
) -> DeliveryCityDTO:
    return DeliveryCityDTO(
        id=delivery_city.id,
        title=delivery_city.title,
    )


def convert_db_model_to_delivery_method_dto(delivery_method: DeliveryMethod) -> DeliveryMethodDTO:
    return DeliveryMethodDTO(
        id=delivery_method.id,
        title=delivery_method.title,
        price=delivery_method.price,
        duration_days=delivery_method.duration_days,
        accompanying_message=delivery_method.accompanying_message,
    )
