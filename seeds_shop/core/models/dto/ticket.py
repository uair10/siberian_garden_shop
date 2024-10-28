import datetime
from dataclasses import dataclass

from seeds_shop.core.models.enums.ticket import TicketStatus

from .user import UserDTO


@dataclass(frozen=True)
class TicketDTO:
    id: int
    status: TicketStatus
    admin: UserDTO
    telegram_id: int
    username: str
    order_id: int
    created_at: datetime.datetime
