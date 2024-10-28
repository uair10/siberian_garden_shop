from sqlalchemy import select
from sqlalchemy.exc import DBAPIError, IntegrityError

from seeds_shop.core.exceptions.common import RepoError
from seeds_shop.core.models.dto.bot_settings import BotSettingsDTO
from seeds_shop.infrastructure.database.converters.bot_settings import convert_db_model_to_bot_settings_dto
from seeds_shop.infrastructure.database.exception_mapper import exception_mapper
from seeds_shop.infrastructure.database.models import BotSettings
from seeds_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class BotSettingsReaderImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_bot_settings(self) -> BotSettingsDTO:
        settings: BotSettings | None = await self._session.scalar(select(BotSettings))
        return convert_db_model_to_bot_settings_dto(settings)


class BotSettingsRepoImpl(SQLAlchemyRepo):
    @exception_mapper
    async def acquire_bot_settings(self) -> BotSettings:
        settings: BotSettings | None = await self._session.scalar(select(BotSettings))

        return settings

    @exception_mapper
    async def update_bot_settings(self, bot_settings: BotSettings) -> None:
        try:
            await self._session.merge(bot_settings)
        except IntegrityError as err:
            self._parse_error(err)

    @staticmethod
    def _parse_error(err: DBAPIError) -> None:
        raise RepoError from err
