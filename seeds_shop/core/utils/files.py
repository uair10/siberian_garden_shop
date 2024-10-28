import os
import tomllib


def get_file_extension(filename: str) -> str:
    """Получаем разрешение файла"""

    _, extension = os.path.splitext(filename)
    return extension.replace(".", "").lower()


def read_toml(path: str) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)
