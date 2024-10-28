from seeds_shop.core.models.dto.shop import ShopDTO
from seeds_shop.infrastructure.database.models import Shop


def convert_db_model_to_shop_dto(shop: Shop) -> ShopDTO:
    return ShopDTO(
        id=shop.id,
        title=shop.title,
        contact_address=shop.contact_address,
    )
