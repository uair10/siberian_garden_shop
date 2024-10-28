from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from seeds_shop.core.models.dto.bot_settings import BotSettingsDTO
from seeds_shop.core.services import BotSettingsService

bot_settings_router = APIRouter(prefix="/bot_settings", tags=["bot_settings"])


@bot_settings_router.get("/")
@inject
async def get_bot_settings(
    bot_settings_service: Annotated[BotSettingsService, FromDishka()],
) -> BotSettingsDTO:
    return await bot_settings_service.get_bot_settings()
