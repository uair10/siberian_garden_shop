from fastapi import FastAPI

from .bot_settings import bot_settings_router
from .cart import cart_router
from .exceptions import setup_exception_handlers
from .healthcheck import healthcheck_router
from .products import products_router
from .promocode import promocode_router
from .users import users_router


def setup_controllers(app: FastAPI) -> None:
    app.include_router(users_router)
    app.include_router(products_router)
    app.include_router(cart_router)
    app.include_router(promocode_router)
    app.include_router(bot_settings_router)
    app.include_router(healthcheck_router)
    setup_exception_handlers(app)
