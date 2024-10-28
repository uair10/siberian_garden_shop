import asyncio
import logging

from seeds_shop.api.main import init_api, run_api
from seeds_shop.core.config import Settings
from seeds_shop.infrastructure.config_loader import load_config
from seeds_shop.infrastructure.logger import configure_logging

logger = logging.getLogger(__name__)


async def main() -> None:
    config = load_config(Settings)
    configure_logging()

    logger.info("Api launched")

    app = init_api(config)
    await run_api(app, config.api)


if __name__ == "__main__":
    asyncio.run(main())
