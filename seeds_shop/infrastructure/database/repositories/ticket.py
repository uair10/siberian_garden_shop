from sqlalchemy import and_, desc, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm import joinedload

from seeds_shop.core.exceptions.common import RepoError
from seeds_shop.core.models.dto.ticket import TicketDTO
from seeds_shop.core.models.enums.ticket import TicketStatus
from seeds_shop.infrastructure.database.converters.ticket import convert_db_model_to_ticket_dto
from seeds_shop.infrastructure.database.exception_mapper import exception_mapper
from seeds_shop.infrastructure.database.models import Ticket, User
from seeds_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class TicketReaderImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_ticket_by_id(self, order_id: int) -> TicketDTO | None:
        """Получаем тикет по id"""

        query = select(Ticket).where(Ticket.id == order_id).options(joinedload(Ticket.admin))
        ticket: Ticket | None = await self._session.scalar(query)

        if not ticket:
            return None

        return convert_db_model_to_ticket_dto(ticket)

    @exception_mapper
    async def get_user_tickets(self, user_tg_id: int) -> list[TicketDTO]:
        """Получаем тикеты, закрепленные за пользователем"""

        query = (
            select(Ticket)
            .outerjoin(Ticket.admin)
            .where(and_(User.telegram_id == user_tg_id, Ticket.status != TicketStatus.closed))
            .order_by(desc(Ticket.created_at))
        )

        res = await self._session.scalars(query)
        tickets: list[Ticket] = list(res)

        return [convert_db_model_to_ticket_dto(ticket) for ticket in tickets]


class TicketRepoImpl(SQLAlchemyRepo):
    @exception_mapper
    async def acquire_ticket_by_id(self, order_id: int) -> Ticket | None:
        """Получаем тикет по id"""

        query = select(Ticket).where(Ticket.id == order_id).options(joinedload(Ticket.admin))
        ticket: Ticket | None = await self._session.scalar(query)

        if not ticket:
            return None

        return ticket

    @exception_mapper
    async def create_ticket(self, ticket: Ticket):
        self._session.add(ticket)
        try:
            await self._session.flush((ticket,))
        except IntegrityError as err:
            self._parse_error(err)

    @exception_mapper
    async def update_ticket(self, ticket: Ticket) -> None:
        try:
            await self._session.merge(ticket)
        except IntegrityError as err:
            self._parse_error(err)

    @staticmethod
    def _parse_error(err: DBAPIError) -> None:
        """Определение ошибки"""

        raise RepoError from err
