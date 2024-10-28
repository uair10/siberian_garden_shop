from seeds_shop.core.models.dto.discount import DiscountDTO
from seeds_shop.infrastructure.database.models import Discount


def convert_db_model_to_discount_dto(discount: Discount) -> DiscountDTO:
    return DiscountDTO(
        id=discount.id,
        category_id=discount.category_id,
        shop_id=discount.shop_id,
        required_quantity=discount.required_quantity,
        discount_percent=discount.discount_percent,
        works_inside_category=discount.works_inside_category,
    )
