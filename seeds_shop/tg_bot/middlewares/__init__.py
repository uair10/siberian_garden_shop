from aiogram import Dispatcher
from dishka import AsyncContainer

from .init_middleware import InitMiddleware
from .locale import LocaleMiddleware
from .throttling import ThrottlingMiddleware


def setup_middlewares(
    dp: Dispatcher,
    container: AsyncContainer,
):
    dp.update.middleware(InitMiddleware(container))
    dp.errors.middleware(InitMiddleware(container))
    dp.update.middleware(LocaleMiddleware())
    dp.errors.middleware(LocaleMiddleware())
    dp.update.middleware(ThrottlingMiddleware())
