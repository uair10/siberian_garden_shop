from datetime import timedelta
from typing import Any

from aiogram import Bot, types
from aiogram_dialog import DialogManager
from arq import ArqRedis

from seeds_shop.core.config import Settings
from seeds_shop.core.models.enums.bot_status import BotStatus
from seeds_shop.core.services import BotSettingsService
from seeds_shop.core.utils.date_time import get_date_time
from seeds_shop.tg_bot.services.tg_helpers import send_tg_message


async def disable_bot(call: types.CallbackQuery, widget: Any, manager: DialogManager):
    bot: Bot = manager.middleware_data.get("bot")
    arq_redis: ArqRedis = manager.middleware_data.get("arqredis")
    config: Settings = manager.middleware_data.get("config")
    bot_settings_service: BotSettingsService = manager.middleware_data.get("bot_settings_service")

    admin_msg = f"Бот отключен до включения админом: {call.from_user.id}"
    bot_disabled_until = None
    if widget.widget_id == "until_morning":
        admin_msg = f"Бот отключен до утра админом: {call.from_user.id}"
        cur_date = get_date_time()
        next_day = cur_date + timedelta(days=1)
        bot_disabled_until = next_day.replace(hour=9, minute=0, second=0, microsecond=0)
        await arq_redis.enqueue_job("auto_enable_bot", _defer_until=bot_disabled_until)

    await bot_settings_service.update_bot_status(BotStatus.DISABLED, bot_disabled_until=bot_disabled_until)
    await send_tg_message(bot, config.tg_bot.admin_channel_id, admin_msg)

    await manager.done()


async def enable_bot(call: types.CallbackQuery, __, manager: DialogManager):
    bot: Bot = manager.middleware_data.get("bot")
    config: Settings = manager.middleware_data.get("config")
    bot_settings_service: BotSettingsService = manager.middleware_data.get("bot_settings_service")

    await bot_settings_service.update_bot_status(BotStatus.ENABLED)

    await send_tg_message(bot, config.tg_bot.admin_channel_id, f"Бот включен админом: {call.from_user.id}")

    await manager.done()
