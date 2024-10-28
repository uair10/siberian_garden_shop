from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Calendar, Cancel

from seeds_shop.tg_bot.dialogs.widgets import LocaleText
from seeds_shop.tg_bot.states.admin import MailingSG

from .handlers import confirm_mailing, get_current_time, set_mailing_date, set_mailing_text, set_mailing_time

mailing_text_window = Window(
    LocaleText("enter-mailing-text-msg"),
    MessageInput(set_mailing_text),
    Cancel(LocaleText("back-btn")),
    state=MailingSG.mailing_text,
)

select_date_window = Window(
    LocaleText("select-mailing-date-msg"),
    Calendar(id="calendar", on_click=set_mailing_date),
    Back(LocaleText("back-btn")),
    state=MailingSG.select_date,
)

select_time_window = Window(
    LocaleText("select-mailing-time-msg"),
    LocaleText("current-time-msg", current_time="{current_time}"),
    TextInput("mailing_time", str, on_success=set_mailing_time),
    Back(LocaleText("back-btn")),
    state=MailingSG.select_time,
    getter=get_current_time,
)

confirm_mailing_window = Window(
    LocaleText("confirm-mailing-msg"),
    Button(LocaleText("yes-btn"), id="yes", on_click=confirm_mailing),
    Button(LocaleText("no-btn"), id="no", on_click=confirm_mailing),
    Back(LocaleText("back-btn")),
    state=MailingSG.confirm_mailing,
)

mailing_dialog = Dialog(
    mailing_text_window,
    select_date_window,
    select_time_window,
    confirm_mailing_window,
)
