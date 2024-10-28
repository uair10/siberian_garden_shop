import logging
from functools import partial

from aiogram import Bot, Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram.types.error_event import ErrorEvent
from aiogram_dialog import DialogManager
from aiogram_dialog.api.exceptions import OutdatedIntent, UnknownIntent
from fluentogram import TranslatorRunner

from seeds_shop.core.exceptions.common import ApplicationException
from seeds_shop.tg_bot.services.tg_helpers import send_msg_with_autodelete

logger = logging.getLogger(__name__)


async def handle_app_errors(error: ErrorEvent, log_chat_id: int, bot: Bot, locale: TranslatorRunner):
    """Обрабатываем ошибки с классом ApplicationException"""

    if c := error.update.callback_query:
        await c.answer(locale.get("unknown-server-error"), show_alert=True)
    else:
        user_id = error.update.message.from_user.id
        if user_id:
            await send_msg_with_autodelete(bot, user_id, locale.get("unknown-server-error"))

    await handle(error=error, log_chat_id=log_chat_id, bot=bot)


async def handle_unexpected_errors(error: ErrorEvent, log_chat_id: int, bot: Bot, locale: TranslatorRunner):
    """Обрабатываем все остальные ошибки"""

    if c := error.update.callback_query:
        await c.answer(locale.get("unknown-server-error"), show_alert=True)
    elif c := error.update.inline_query:
        await send_msg_with_autodelete(bot, c.from_user.id, locale.get("unknown-server-error"))
    else:
        await send_msg_with_autodelete(bot, error.update.message.from_user.id, locale.get("unknown-server-error"))
    await handle(error=error, log_chat_id=log_chat_id, bot=bot)


async def clear_unknown_intent(error: ErrorEvent, dialog_manager: DialogManager, bot: Bot):
    """Обрабатываем ошибку aiogram dialog UnknownIntent"""

    await dialog_manager.reset_stack(True)
    assert error.update.callback_query
    assert error.update.callback_query.message
    await bot.edit_message_reply_markup(
        chat_id=error.update.callback_query.message.chat.id,
        message_id=error.update.callback_query.message.message_id,
        reply_markup=None,
    )


async def handle(error: ErrorEvent, log_chat_id: int, bot: Bot):
    """Отправляем ошибку в чат для логов"""

    error_name = error.exception.__class__.__name__
    logger.exception(
        "Cause unexpected exception %s, by processing %s",
        error_name,
        error.update.model_dump(exclude_none=True),
        exc_info=error.exception,
    )
    if not log_chat_id:
        return

    await bot.send_message(
        log_chat_id,
        f"Получено исключение {error_name}\nВо время обработки апдейта ",
    )


def setup_error_handlers(dp: Dispatcher, log_chat_id: int):
    dp.errors.register(
        partial(handle_app_errors, log_chat_id=log_chat_id),
        ExceptionTypeFilter(ApplicationException),
    )
    dp.errors.register(clear_unknown_intent, ExceptionTypeFilter(UnknownIntent, OutdatedIntent))
    dp.errors.register(
        partial(handle_unexpected_errors, log_chat_id=log_chat_id),
        ExceptionTypeFilter(Exception),
    )
    dp.errors.register(partial(handle, log_chat_id=log_chat_id))
