import asyncio
import contextlib
import logging

from aiogram import Bot, exceptions, types

from seeds_shop.core.models.dto.user import UserDTO

logger = logging.getLogger(__name__)


async def send_tg_message(
    bot: Bot,
    user_id: int,
    text: str,
    disable_notification: bool = False,
    **kwargs,
) -> bool | types.Message:
    """Безопасно отправляем сообщение пользователю"""

    try:
        msg = await bot.send_message(user_id, text, disable_notification=disable_notification, **kwargs)
    except exceptions.TelegramForbiddenError:
        logger.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logger.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds.")
        await asyncio.sleep(e.retry_after)
        return await send_tg_message(bot, user_id, text)  # Recursive call
    except exceptions.TelegramAPIError:
        logger.error(f"Target [ID:{user_id}]: failed")
    else:
        logger.info(f"Target [ID:{user_id}]: success")
        return msg
    return False


async def send_msg_copy(
    bot: Bot,
    user_id: int,
    message: types.Message,
) -> bool:
    try:
        await message.copy_to(user_id).as_(bot)
    except exceptions.TelegramForbiddenError:
        logger.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logger.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds.")
        await asyncio.sleep(e.retry_after)
        return await send_msg_copy(bot, user_id, message)  # Recursive call
    except exceptions.TelegramAPIError:
        logger.error(f"Target [ID:{user_id}]: failed")
    else:
        logger.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcast(
    bot: Bot,
    users: list[int | UserDTO],
    message: types.Message | str,
    **kwargs,
) -> tuple[int, int]:
    """
    Рассылка по пользователям
    :param bot: aiogram.Bot instance
    :param users: Список telegram id или список Users
    :param message: Сообщение или текст для отправки
    :return: Успешно отправлено сообщений, сообщений с ошибкой
    """
    messages_sent = 0
    errors_count = 0

    try:
        for user in users:
            if isinstance(user, UserDTO):
                user = user.telegram_id
            if isinstance(message, str):
                if await send_tg_message(bot, user, message, **kwargs):
                    messages_sent += 1
                else:
                    errors_count += 1
            elif await send_msg_copy(bot, user, message):
                messages_sent += 1
            else:
                errors_count += 1
            await asyncio.sleep(0.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        logger.info(
            f"{messages_sent} messages successful sent. With errors: {errors_count}. Planned to send total: {len(users)}",
        )

    return messages_sent, errors_count


async def delete_msg(msg: types.Message) -> None:
    """Безопасно удаляем сообщение"""

    with contextlib.suppress(exceptions.TelegramBadRequest):
        await msg.delete()


async def delete_msg_by_id(bot: Bot, message_id: int, chat_id: int) -> None:
    """Безопасно удаляем сообщение по id"""

    with contextlib.suppress(exceptions.TelegramBadRequest):
        await bot.delete_message(chat_id, message_id)


async def answer_msg_with_autodelete(message: types.Message, text: str, seconds: int = 2) -> None:
    """
    Отвечаем на сообщение с автоудалением
    :param message: Сообщение, на которое нужно ответить
    :param text: Текст ответа
    :param seconds: Через сколько секунд удалить ответ
    @return:
    """

    msg = await message.answer(text)
    await asyncio.sleep(seconds)
    await delete_msg(msg)


async def send_msg_with_autodelete(bot: Bot, user_id: int, text: str, seconds: int = 2) -> None:
    """
    Отправляем сообщение с автоудалением
    :param bot: Инстанс бота
    :param user_id: Telegram id пользователя
    :param text: Текст сообщения
    :param seconds: Через сколько секунд удалить ответ
    @return:
    """

    msg = await send_tg_message(bot, user_id=user_id, text=text)
    await asyncio.sleep(seconds)
    await delete_msg(msg)
