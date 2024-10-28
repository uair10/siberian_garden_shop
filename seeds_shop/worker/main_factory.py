from dishka import AsyncContainer, Provider, make_async_container

from seeds_shop.infrastructure.di import get_providers


def create_container() -> AsyncContainer:
    container = make_async_container(*get_worker_providers())
    return container


def get_worker_providers() -> list[Provider]:
    return [
        *get_providers(),
    ]
