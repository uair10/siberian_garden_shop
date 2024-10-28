from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, WebApp
from aiogram_dialog.widgets.text import Format

from seeds_shop.core.models.enums.user import UserRole
from seeds_shop.tg_bot.dialogs.getters.users import user_info_getter, user_role_getter
from seeds_shop.tg_bot.dialogs.getters.webapp import webapp_info_getter
from seeds_shop.tg_bot.dialogs.widgets import LocaleText
from seeds_shop.tg_bot.states import ClientSG, UserOrdersSG
from seeds_shop.tg_bot.states.admin import AdminSG
from seeds_shop.tg_bot.states.user import LanguageSG

start_window = Window(
    LocaleText("welcome", user="{event.from_user.username}"),
    WebApp(text=LocaleText("catalog-btn"), url=Format("{webapp_url}")),
    Start(
        LocaleText("orders-btn"),
        id="my_orders",
        state=UserOrdersSG.orders_history,
        when=F["user_orders_count"] > 0,
    ),
    Start(LocaleText("change-lang-btn"), "change_lang_btn", LanguageSG.select_language),
    Start(
        LocaleText("admin-btn"),
        id="admin_panel",
        when=(F["user_role"].in_([UserRole.admin, UserRole.stuff])),
        state=AdminSG.admin,
    ),
    state=ClientSG.start,
    getter=(user_info_getter, user_role_getter, webapp_info_getter),
)


start_dialog = Dialog(start_window)
