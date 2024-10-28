import logging

from seeds_shop.core.models.dto.ticket import TicketDTO
from seeds_shop.core.models.enums.ticket import TicketStatus
from seeds_shop.infrastructure.database.converters.ticket import convert_db_model_to_ticket_dto
from seeds_shop.infrastructure.database.models import Ticket, User
from seeds_shop.infrastructure.database.uow import SQLAlchemyUoW

logger = logging.getLogger(__name__)


class TicketService:
    def __init__(self, uow: SQLAlchemyUoW):
        self._uow = uow

    async def get_ticket_by_id(self, ticket_id: int) -> TicketDTO | None:
        """Получаем тикет по id"""

        return await self._uow.ticket_reader.get_ticket_by_id(ticket_id)

    async def get_user_tickets(self, user_tg_id: int) -> list[TicketDTO]:
        """Получаем тикеты, закрепленные за  пользователем"""

        return await self._uow.ticket_reader.get_user_tickets(user_tg_id)

    async def create_ticket(self, user_tg_id: int, username: str, order_id: int) -> TicketDTO:
        """Создаем тикет"""

        ticket = Ticket(telegram_id=user_tg_id, username=username, order_id=order_id)

        await self._uow.ticket_repo.create_ticket(ticket)
        await self._uow.commit()

        logger.info(f"Ticket {ticket} was created")

        return convert_db_model_to_ticket_dto(ticket)

    async def assign_ticket_to_admin(self, ticket_id: int, user_tg_id: int) -> None:
        """Присваиваем тикет админу"""

        ticket: Ticket = await self._uow.ticket_repo.acquire_ticket_by_id(ticket_id)
        user: User = await self._uow.user_repo.acquire_user_by_tg_id(user_tg_id)
        ticket.admin = user

        await self._uow.ticket_repo.update_ticket(ticket)
        await self._uow.commit()

        logger.info(f"Ticket {ticket} was assigned to {user_tg_id}")

    async def close_ticket(self, ticket_id: int) -> None:
        """Закрываем тикет"""

        ticket: Ticket = await self._uow.ticket_repo.acquire_ticket_by_id(ticket_id)
        ticket.status = TicketStatus.closed

        await self._uow.ticket_repo.update_ticket(ticket)
        await self._uow.commit()

        logger.info(f"Ticket {ticket} was closed")
