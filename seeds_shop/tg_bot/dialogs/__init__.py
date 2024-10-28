from aiogram import Dispatcher

from seeds_shop.tg_bot.dialogs import admin, common


def register_dialogs(dp: Dispatcher):
    common.register_common_dialogs(dp)
    admin.register_admin_dialogs(dp)
