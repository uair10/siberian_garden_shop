from dataclasses import dataclass

from seeds_shop.core.models.dto.user import UserDTO


@dataclass
class UserWithBonuses:
    user: UserDTO
    bonuses: int
