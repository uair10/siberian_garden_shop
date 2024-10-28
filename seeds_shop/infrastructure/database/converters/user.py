from seeds_shop.core.models.dto.user import UserDTO
from seeds_shop.infrastructure.database.models import User


def convert_db_model_to_user_dto(user: User) -> UserDTO:
    return UserDTO(
        username=user.username,
        telegram_id=user.telegram_id,
        id=user.id,
        role=user.role,
        delivery_zone_id=user.delivery_zone_id,
        lang_code=user.lang_code,
        created_at=user.created_at,
    )
