import logging
from datetime import date, datetime
from typing import Any

from aiogram import types
from aiogram_dialog import DialogManager
from arq import ArqRedis
from fluentogram import TranslatorRunner

from seeds_shop.core.utils.date_time import get_date_time

logger = logging.getLogger(__name__)


async def get_current_time(dialog_manager: DialogManager, **kwargs):
    return {"current_time": get_date_time().time()}


async def set_mailing_text(message: types.Message, __, manager: DialogManager, **kwargs):
    manager.dialog_data["mailing_message"] = message.model_dump_json()
    await manager.next()


async def set_mailing_date(_, __, manager: DialogManager, selected_date: date):
    manager.dialog_data["mailing_date"] = str(selected_date)

    await manager.next()


async def set_mailing_time(message: types.Message, _, manager: DialogManager, mailing_time: str):
    locale: TranslatorRunner = manager.middleware_data.get("locale")

    try:
        datetime.strptime(mailing_time, "%H:%M:%S")
    except ValueError:
        await message.answer(locale.get("wrong-time-format-msg"))
        return

    manager.dialog_data["mailing_time"] = mailing_time

    await manager.next()


async def confirm_mailing(call: types.CallbackQuery, widget: Any, manager: DialogManager):
    arqredis: ArqRedis = manager.middleware_data.get("arqredis")
    locale: TranslatorRunner = manager.middleware_data.get("locale")

    selected_date: str = manager.dialog_data.get("mailing_date")
    mailing_time: str = manager.dialog_data.get("mailing_time")

    date_and_time = datetime.combine(
        datetime.strptime(selected_date, "%Y-%m-%d").date(),
        datetime.strptime(mailing_time, "%H:%M:%S").time(),
    )

    if widget.widget_id == "yes":
        await arqredis.enqueue_job(
            "notify_users",
            _defer_until=date_and_time,
            message=types.Message.model_validate_json(manager.dialog_data.get("mailing_message")),
        )

        logger.info("В планировщик добавлена задача на рассылку")
        await call.answer(locale.get("mailing-planned-msg"))

    elif widget.widget_id == "no":
        await call.answer(locale.get("mailing-cancelled-msg"))

    await manager.done()
