from seeds_shop.core.models.dto.ticket import TicketDTO
from seeds_shop.infrastructure.database.models import Ticket


def convert_db_model_to_ticket_dto(ticket: Ticket) -> TicketDTO:
    return TicketDTO(
        id=ticket.id,
        status=ticket.status,
        admin=ticket.admin,
        telegram_id=ticket.telegram_id,
        username=ticket.username,
        order_id=ticket.order_id,
        created_at=ticket.created_at,
    )
