import logging

import uvicorn
from cashews import cache
from fastapi import FastAPI

from seeds_shop.api.controllers import setup_controllers
from seeds_shop.api.dependencies import setup_di
from seeds_shop.api.middlewares import setup_middlewares
from seeds_shop.core.config import ApiConfig, Settings
from seeds_shop.infrastructure.logger import configure_logging

logger = logging.getLogger(__name__)


def init_api(config: Settings) -> FastAPI:
    configure_logging()

    app = FastAPI(debug=config.api.debug)

    setup_middlewares(app, config.api)
    setup_di(app)
    cache.setup(config.redis.url)
    setup_controllers(app)

    logger.info("API initialized")

    return app


async def run_api(app: FastAPI, api_config: ApiConfig) -> None:
    config = uvicorn.Config(
        app,
        host=api_config.host,
        port=api_config.port,
        log_level=api_config.log_level,
        log_config=None,
    )
    server = uvicorn.Server(config)
    logger.info("Running API")

    await server.serve()
