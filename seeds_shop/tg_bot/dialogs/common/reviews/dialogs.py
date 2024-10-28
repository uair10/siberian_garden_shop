from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel

from seeds_shop.tg_bot.dialogs.widgets import LocaleText
from seeds_shop.tg_bot.states.user import LeaveReviewSG

from .handlers import leave_review

enter_review_text_window = Window(
    LocaleText("enter-review-text-msg"),
    TextInput("review_text", str, on_success=leave_review),
    Cancel(LocaleText("back-btn")),
    state=LeaveReviewSG.enter_review_text,
)

reviews_dialog = Dialog(enter_review_text_window)
