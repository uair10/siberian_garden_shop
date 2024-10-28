from aiogram import Dispatcher

from .create_order import create_order_dialog
from .language import language_dialog
from .orders import order_details_dialog, orders_history_dialog
from .profile import user_profile_dialog
from .reviews import reviews_dialog
from .start import start_dialog


def register_common_dialogs(dp: Dispatcher):
    dp.include_router(start_dialog)
    dp.include_router(language_dialog)
    dp.include_router(user_profile_dialog)
    dp.include_router(create_order_dialog)
    dp.include_router(orders_history_dialog)
    dp.include_router(order_details_dialog)
    dp.include_router(reviews_dialog)
