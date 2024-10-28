from dataclasses import dataclass


@dataclass(frozen=True)
class CategoryDTO:
    id: int
    title: str
    position_number: int
