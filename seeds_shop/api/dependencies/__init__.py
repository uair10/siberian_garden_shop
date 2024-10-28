from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from seeds_shop.infrastructure.di import get_providers


def setup_di(app: FastAPI):
    container = make_async_container(*get_providers())
    setup_dishka(container, app)
