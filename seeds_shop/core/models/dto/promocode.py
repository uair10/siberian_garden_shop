from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class PromocodeDTO:
    id: int
    name: str
    amount: Decimal
    limit: int
    reusable: bool
    uses_number: int
