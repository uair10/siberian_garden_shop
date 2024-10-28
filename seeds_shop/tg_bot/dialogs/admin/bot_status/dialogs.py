from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Next
from aiogram_dialog.widgets.text import Const

from seeds_shop.tg_bot.dialogs.admin.bot_status.handlers import disable_bot, enable_bot
from seeds_shop.tg_bot.dialogs.getters.bot_status import bot_status_getter
from seeds_shop.tg_bot.dialogs.widgets import LocaleText
from seeds_shop.tg_bot.states import BotStatusSG

display_bot_status_window = Window(
    LocaleText("bot-status") + Const("🟢", when=F["is_bot_enabled"]) + Const("🔴", when=~F["is_bot_enabled"]),
    LocaleText("bot-disabled-until", bot_disabled_until="{bot_disabled_until}", when=F["bot_disabled_until"]),
    Button(LocaleText("enable-bot-btn"), "enable_bot", on_click=enable_bot, when=~F["is_bot_enabled"]),
    Next(LocaleText("disable-bot-btn"), when=F["is_bot_enabled"]),
    Cancel(LocaleText("back-btn")),
    state=BotStatusSG.display_bot_status,
    getter=bot_status_getter,
)

disable_bot_window = Window(
    LocaleText("select-bot-disable-type"),
    Button(LocaleText("until-enabled-btn"), id="until_enabled", on_click=disable_bot),
    Button(LocaleText("until-morning-btn"), id="until_morning", on_click=disable_bot),
    Back(LocaleText("back-btn")),
    state=BotStatusSG.select_disable_type,
)

bot_status_dialog = Dialog(display_bot_status_window, disable_bot_window)
