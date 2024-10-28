from aiogram import Bot
from aiogram.enums import ParseMode
from dishka import Provider, Scope, provide

from seeds_shop.core.config import TgBotConfig


class BotProvider(Provider):
    scope = Scope.APP

    @provide
    def get_bot(self, bot_config: TgBotConfig) -> Bot:
        bot = Bot(
            token=bot_config.token,
            parse_mode=ParseMode.HTML,
        )
        return bot
