from aiogram_dialog import DialogManager

from seeds_shop.core.config import Settings


async def webapp_info_getter(dialog_manager: DialogManager, config: Settings, **kwargs):
    return {"webapp_url": config.tg_bot.webapp_url}
