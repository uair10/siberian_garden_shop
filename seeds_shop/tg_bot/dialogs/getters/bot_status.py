from aiogram_dialog import DialogManager

from seeds_shop.core.services import BotSettingsService


async def bot_status_getter(
    dialog_manager: DialogManager,
    bot_settings_service: BotSettingsService,
    **kwargs,
):
    bot_settings = await bot_settings_service.get_bot_settings()

    return {
        "is_bot_enabled": bot_settings.is_bot_enabled,
        "bot_disabled_until": bot_settings.bot_disabled_until,
    }
