from aiogram.fsm.state import State, StatesGroup


class AdminSG(StatesGroup):
    admin = State()


class MailingSG(StatesGroup):
    mailing_text = State()
    select_date = State()
    select_time = State()
    confirm_mailing = State()


class TicketsSG(StatesGroup):
    tickets_history = State()


class TicketDetailsSG(StatesGroup):
    ticket_details = State()
    confirm_closing_ticket = State()
    confirm_closing_order = State()
    confirm_cancel_order = State()


class BotStatusSG(StatesGroup):
    display_bot_status = State()
    select_disable_type = State()
