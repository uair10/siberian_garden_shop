from aiogram import types
from aiogram_dialog import DialogManager, StartMode

from seeds_shop.core.exceptions.user import UserTgIdNotExist
from seeds_shop.core.services import StatsService, UserService
from seeds_shop.tg_bot.states import ClientSG


async def user_start(
    message: types.Message | types.CallbackQuery,
    dialog_manager: DialogManager,
    user_service: UserService,
    stats_service: StatsService,
):
    """Команда старта для пользователей"""

    user_id = message.from_user.id
    username = message.from_user.username
    if not username:
        username = message.from_user.first_name

    try:
        await user_service.get_user_by_telegram_id(user_id)
    except UserTgIdNotExist:
        await user_service.create_user(
            telegram_id=user_id,
            username=username,
        )
        await stats_service.add_stats(users_registered=1)

    if isinstance(message, types.CallbackQuery):
        await message.message.delete()
    else:
        await dialog_manager.start(ClientSG.start, mode=StartMode.RESET_STACK)
