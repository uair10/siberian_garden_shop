from seeds_shop.core.models.dto.category import CategoryDTO
from seeds_shop.infrastructure.database.models import Category


def convert_db_model_to_category_dto(category: Category) -> CategoryDTO:
    return CategoryDTO(id=category.id, title=category.title, position_number=category.position_number)
