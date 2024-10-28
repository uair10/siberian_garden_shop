from seeds_shop.core.models.dto.promocode import PromocodeDTO
from seeds_shop.infrastructure.database import models


def convert_db_model_to_promocode_dto(promocode: models.Promocode) -> PromocodeDTO:
    return PromocodeDTO(
        id=promocode.id,
        name=promocode.name,
        amount=promocode.amount,
        limit=promocode.limit,
        reusable=promocode.reusable,
        uses_number=promocode.uses_number,
    )
