from aiogram import Dispatcher, F
from aiogram.filters import Command

from seeds_shop.core.config import TgBotConfig
from seeds_shop.tg_bot.handlers.errors import setup_error_handlers
from seeds_shop.tg_bot.handlers.inline_query import inline_response
from seeds_shop.tg_bot.handlers.order import go_to_order_handler, resend_stuff_msg, start_order_create
from seeds_shop.tg_bot.handlers.start import user_start
from seeds_shop.tg_bot.handlers.support import contact_support, take_ticket
from seeds_shop.tg_bot.keyboards.inline import ConfirmCartCF, OrderCF, SupportCF, TicketCF


def register_handlers(dp: Dispatcher, config: TgBotConfig):
    dp.message.register(user_start, Command(commands="start"))
    dp.callback_query.register(user_start, F.data == "go_to_shopping")
    dp.callback_query.register(start_order_create, ConfirmCartCF.filter())
    dp.callback_query.register(contact_support, SupportCF.filter())
    dp.callback_query.register(go_to_order_handler, OrderCF.filter(F.action == "go_to_order"))
    dp.callback_query.register(resend_stuff_msg, F.data == "hold_off")
    dp.callback_query.register(take_ticket, TicketCF.filter())
    dp.inline_query.register(inline_response)

    setup_error_handlers(dp, config.developer_id)
