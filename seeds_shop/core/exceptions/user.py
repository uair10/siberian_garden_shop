from dataclasses import dataclass

from seeds_shop.core.exceptions.common import ApplicationException


@dataclass
class UserIdNotExist(ApplicationException):
    ...


@dataclass
class UserNameNotExist(ApplicationException):
    ...


@dataclass
class UserTgIdNotExist(ApplicationException):
    @property
    def message(self) -> str:
        return "User not found"


@dataclass
class UserIdAlreadyExist(ApplicationException):
    ...


@dataclass
class UserTgIdAlreadyExist(ApplicationException):
    ...
