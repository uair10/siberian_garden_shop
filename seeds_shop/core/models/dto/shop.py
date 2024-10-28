from dataclasses import dataclass


@dataclass(frozen=True)
class ShopDTO:
    id: int
    title: str
    contact_address: str
