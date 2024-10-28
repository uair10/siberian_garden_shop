from typing import Annotated

from cashews import cache
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette import status

from seeds_shop.api.controllers.responses.users import UserWithBonuses
from seeds_shop.core.models.dto.user import UserDTO
from seeds_shop.core.services import BonusService, BotSettingsService, UserService

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": UserWithBonuses},
    },
)
@inject
async def get_user_by_telegram_id(
    user_tg_id: int,
    user_service: Annotated[UserService, FromDishka()],
    bonus_service: Annotated[BonusService, FromDishka()],
    bot_settings_service: Annotated[BotSettingsService, FromDishka()],
) -> UserWithBonuses:
    user = await user_service.get_user_by_telegram_id(user_tg_id)
    settings = await bot_settings_service.get_bot_settings()
    user_bonuses = await bonus_service.get_user_bonus_balance(user.id, settings.days_before_using_bonus)

    return UserWithBonuses(user=user, bonuses=user_bonuses)


@users_router.get(
    "/get_by_username",
    responses={
        status.HTTP_200_OK: {"model": UserDTO},
    },
)
@cache(ttl="1m", key="user_info:{username}")
@inject
async def get_user_by_username(
    username: str,
    user_service: Annotated[UserService, FromDishka()],
) -> UserDTO:
    return await user_service.get_user_by_username(username)
