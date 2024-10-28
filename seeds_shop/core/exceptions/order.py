from dataclasses import dataclass

from seeds_shop.core.exceptions.common import ApplicationException


@dataclass
class OrderIdNotExist(ApplicationException):
    ...


@dataclass
class OrderIdAlreadyExist(ApplicationException):
    ...


@dataclass
class ProductNotExists(ApplicationException):
    ...


@dataclass
class InsufficientStock(ApplicationException):
    product_id: int
    requested_amount: int
    available_amount: int

    @property
    def message(self) -> str:
        return "The quantity of goods in stock is less than requested. Try again later"
