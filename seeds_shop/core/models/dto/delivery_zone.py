from dataclasses import dataclass


@dataclass(frozen=True)
class DeliveryZoneDTO:
    id: int
    title: str | None = None
