from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Group
from aiogram_dialog.widgets.text import Const

from seeds_shop.tg_bot.dialogs.widgets import LocaleText
from seeds_shop.tg_bot.states.user import LanguageSG

from .handlers import set_user_language

language_window = Window(
    LocaleText("select-lang-msg"),
    Group(
        Button(Const("🇺🇸 English"), id="en", on_click=set_user_language),
        Button(Const("🇷🇺 Русский"), id="ru", on_click=set_user_language),
        width=2,
    ),
    Cancel(LocaleText("back-btn")),
    state=LanguageSG.select_language,
)

language_dialog = Dialog(language_window)
