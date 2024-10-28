from seeds_shop.core.models.dto.promocode import PromocodeDTO
from seeds_shop.infrastructure.database.uow import SQLAlchemyUoW


class PromocodeService:
    def __init__(self, uow: SQLAlchemyUoW):
        self._uow = uow

    async def get_promocode_by_id(self, promocode_id: int) -> PromocodeDTO:
        return await self._uow.promocode_reader.get_promocode_by_id(promocode_id)

    async def get_promocode_by_name(self, promocode_name: str) -> PromocodeDTO:
        """Ищем промокод по имени"""
        return await self._uow.promocode_reader.get_promocode_by_name(promocode_name)

    async def increase_promocode_uses(self, promocode_id: int, uses: int = 1) -> None:
        promocode = await self._uow.promocode_repo.acquire_promocode_by_id(promocode_id)
        promocode.uses_number += uses

        await self._uow.promocode_repo.update_promocode(promocode)

        await self._uow.commit()
