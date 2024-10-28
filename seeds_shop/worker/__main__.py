import asyncio
import logging
from typing import Any

import pytz
from arq import cron
from arq.worker import create_worker
from dishka.integrations.arq import setup_dishka

from seeds_shop.core.config import RedisConfig, Settings
from seeds_shop.infrastructure.logger import configure_logging
from seeds_shop.worker.jobs import (
    auto_enable_bot,
    notify_expired_payment,
    notify_expiring_payment,
    notify_user,
    notify_users,
    send_cart_confirmation_msg,
)
from seeds_shop.worker.jobs.auto_close_orders import auto_close_completed_orders, free_stock_in_cancelled_orders
from seeds_shop.worker.main_factory import create_container

logger = logging.getLogger(__name__)


def create_worker_settings(redis_config: RedisConfig) -> dict[str, Any]:
    return {
        "functions": [
            notify_users,
            notify_user,
            send_cart_confirmation_msg,
            notify_expired_payment,
            notify_expiring_payment,
            free_stock_in_cancelled_orders,
            auto_close_completed_orders,
            auto_enable_bot,
        ],
        "timezone": pytz.timezone("Europe/Moscow"),
        "allow_abort_jobs": True,
        "redis_settings": redis_config.pool_settings,
        "cron_jobs": [
            cron(
                free_stock_in_cancelled_orders,
                microsecond=0,
                max_tries=2,
                run_at_startup=True,
            ),
            cron(
                auto_close_completed_orders,
                microsecond=0,
                max_tries=2,
                run_at_startup=True,
            ),
        ],
    }


async def main():
    configure_logging()
    container = create_container()

    config = await container.get(Settings)
    worker_settings = create_worker_settings(config.redis)
    worker = create_worker(worker_settings)
    setup_dishka(container, worker_settings=worker)

    try:
        logger.info("Starting worker")
        await worker.async_run()
    finally:
        logger.info("Worker stopped")
        await container.close()
        await worker.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except asyncio.CancelledError:
        pass
