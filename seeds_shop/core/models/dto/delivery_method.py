from dataclasses import dataclass
from decimal import Decimal


@dataclass
class DeliveryMethodDTO:
    id: int
    title: str
    price: Decimal
    duration_days: int
    accompanying_message: str


@dataclass
class DeliveryCityDTO:
    id: int
    title: str
