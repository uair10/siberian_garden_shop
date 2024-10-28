import enum


class UserRole(enum.Enum):
    user = "user"
    stuff = "stuff"  # Сотрудник склада
    admin = "admin"


class LangCode(enum.Enum):
    ru = "ru"
    en = "en"
