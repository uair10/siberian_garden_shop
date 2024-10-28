from seeds_shop.core.models.dto.bot_settings import BotSettingsDTO
from seeds_shop.infrastructure.database.models import BotSettings


def convert_db_model_to_bot_settings_dto(bot_settings: BotSettings) -> BotSettingsDTO:
    return BotSettingsDTO(
        is_bot_enabled=bot_settings.is_bot_enabled,
        bot_disabled_until=bot_settings.bot_disabled_until,
        days_before_using_bonus=bot_settings.days_before_using_bonus,
        maximum_bonus_discount_percent=bot_settings.maximum_bonus_discount_percent,
        maximum_bonus_for_order_percent=bot_settings.maximum_bonus_for_order_percent,
        paid_delivery_enabled=bot_settings.paid_delivery_enabled,
        free_delivery_threshold=bot_settings.free_delivery_threshold,
    )
