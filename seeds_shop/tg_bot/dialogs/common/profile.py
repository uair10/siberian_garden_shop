from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, Start

from seeds_shop.tg_bot.dialogs.getters.users import user_info_getter
from seeds_shop.tg_bot.dialogs.widgets import LocaleText
from seeds_shop.tg_bot.states.user import UserOrdersSG, UserProfileSG

user_profile_window = Window(
    LocaleText("your-account"),
    LocaleText("registered_date", reg_date="{reg_date}"),
    Start(LocaleText("orders-btn"), id="my_orders", state=UserOrdersSG.orders_history),
    Cancel(LocaleText("back-btn")),
    state=UserProfileSG.show_profile,
    getter=user_info_getter,
)

user_profile_dialog = Dialog(
    user_profile_window,
)
