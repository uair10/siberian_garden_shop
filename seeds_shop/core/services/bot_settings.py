import datetime

from seeds_shop.core.models.dto.bot_settings import BotSettingsDTO
from seeds_shop.core.models.enums.bot_status import BotStatus
from seeds_shop.infrastructure.database.models import BotSettings
from seeds_shop.infrastructure.database.uow import SQLAlchemyUoW


class BotSettingsService:
    def __init__(self, uow: SQLAlchemyUoW):
        self._uow = uow

    async def get_bot_settings(self) -> BotSettingsDTO:
        """Получаем настройки бота"""

        return await self._uow.bot_settings_reader.get_bot_settings()

    async def update_bot_status(self, bot_status: BotStatus, bot_disabled_until: datetime.datetime | None = None):
        """Включаем/выключаем бота"""

        bot_settings: BotSettings = await self._uow.bot_settings_repo.acquire_bot_settings()
        bot_settings.is_bot_enabled = bot_status.value
        bot_settings.bot_disabled_until = bot_disabled_until

        await self._uow.bot_settings_repo.update_bot_settings(bot_settings)

        await self._uow.commit()
