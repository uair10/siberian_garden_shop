import asyncio
import logging

from aiogram import Bot, Dispatcher

from seeds_shop.core.config import Settings
from seeds_shop.infrastructure.logger import configure_logging
from seeds_shop.tg_bot.main_factory import create_container
from seeds_shop.tg_bot.services.tg_helpers import send_tg_message

logger = logging.getLogger(__name__)


async def main():
    container = create_container()
    bot = await container.get(Bot)
    dp = await container.get(Dispatcher)
    config = await container.get(Settings)
    configure_logging(config.logging)

    bot_username = await bot.get_me()
    logger.error(f"Starting bot {bot_username}")

    await send_tg_message(bot, config.tg_bot.developer_id, "Бот запущен!")
    try:
        await dp.start_polling(bot)
    finally:
        logger.info("Bot stopped")
        await container.close()


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
