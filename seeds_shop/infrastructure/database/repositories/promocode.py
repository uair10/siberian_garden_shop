from sqlalchemy import select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm import joinedload

from seeds_shop.core.exceptions.common import RepoError
from seeds_shop.core.models.dto.promocode import PromocodeDTO
from seeds_shop.infrastructure.database.converters.promocode import convert_db_model_to_promocode_dto
from seeds_shop.infrastructure.database.exception_mapper import exception_mapper
from seeds_shop.infrastructure.database.models import Promocode
from seeds_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class PromocodeReaderImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_promocode_by_id(self, promocode_id: int) -> PromocodeDTO | None:
        query = select(Promocode).where(Promocode.id == promocode_id)
        promocode: Promocode | None = await self._session.scalar(query)

        if not promocode:
            return None

        return convert_db_model_to_promocode_dto(promocode)

    @exception_mapper
    async def get_promocode_by_name(self, promocode_name: int) -> PromocodeDTO | None:
        """Ищем промокод по имени"""

        query = select(Promocode).where(Promocode.name == promocode_name).options(joinedload(Promocode.users))
        promocode: Promocode | None = await self._session.scalar(query)

        if not promocode:
            return None

        return convert_db_model_to_promocode_dto(promocode)


class PromocodeRepoImpl(SQLAlchemyRepo):
    @exception_mapper
    async def acquire_promocode_by_id(self, promocode_id: int) -> PromocodeDTO | None:
        query = select(Promocode).where(Promocode.id == promocode_id)
        promocode: Promocode | None = await self._session.scalar(query)

        if not promocode:
            return None

        return convert_db_model_to_promocode_dto(promocode)

    @exception_mapper
    async def update_promocode(self, promocode: Promocode) -> None:
        try:
            await self._session.merge(promocode)
        except IntegrityError as err:
            self._parse_error(err)

    @staticmethod
    def _parse_error(err: DBAPIError) -> None:
        raise RepoError from err
