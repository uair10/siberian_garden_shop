import datetime
from dataclasses import dataclass

from seeds_shop.core.models.enums.user import LangCode, UserRole


@dataclass(frozen=True)
class UserDTO:
    id: int
    telegram_id: int
    username: str
    role: UserRole | None = None
    delivery_zone_id: int | None = None
    lang_code: LangCode | None = None
    created_at: datetime.datetime | None = None
