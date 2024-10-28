import os
from typing import TypeVar

from pydantic import TypeAdapter

from seeds_shop.core.utils.files import read_toml

T = TypeVar("T")
DEFAULT_CONFIG_PATH = "./config/config.dev.toml"


def load_config(config_type: type[T], config_scope: str | None = None, path: str | None = None) -> T:
    if path is None:
        path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)

    data = read_toml(path)

    if config_scope is not None:
        data = data[config_scope]

    return TypeAdapter(type=config_type).validate_python(data)
