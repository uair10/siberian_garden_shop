from typing import Annotated, Any

from aiogram import Bot
from dishka import FromDishka
from dishka.integrations.arq import inject

from seeds_shop.core.config import Settings
from seeds_shop.core.models.enums.bot_status import BotStatus
from seeds_shop.core.services import BotSettingsService
from seeds_shop.tg_bot.services.tg_helpers import send_tg_message
from seeds_shop.worker.exception_handler import exception_handler


@exception_handler
@inject
async def auto_enable_bot(
    context: dict[Any, Any],
    bot: Annotated[Bot, FromDishka()],
    config: Annotated[Settings, FromDishka()],
    bot_settings_service: Annotated[BotSettingsService, FromDishka()],
) -> None:
    await bot_settings_service.update_bot_status(BotStatus.ENABLED)

    await send_tg_message(bot, config.tg_bot.admin_channel_id, "Бот был автоматически включен")
