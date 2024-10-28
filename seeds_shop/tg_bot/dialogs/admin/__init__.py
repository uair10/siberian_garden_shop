from aiogram import Dispatcher

from .bot_status import bot_status_dialog
from .mailing import mailing_dialog
from .start import features_dialog
from .tickets import ticket_details_dialog, tickets_history_dialog


def register_admin_dialogs(dp: Dispatcher):
    dp.include_router(features_dialog)
    dp.include_router(mailing_dialog)
    dp.include_router(tickets_history_dialog)
    dp.include_router(ticket_details_dialog)
    dp.include_router(bot_status_dialog)
