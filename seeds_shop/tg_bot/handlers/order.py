from datetime import timedelta

from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram_dialog import DialogManager
from arq import ArqRedis

from seeds_shop.tg_bot.services.tg_helpers import delete_msg
from seeds_shop.tg_bot.states import CreateOrderSG, OrderDetailsSG


async def start_order_create(
    call: types.CallbackQuery,
    callback_data: CallbackData,
    dialog_manager: DialogManager,
):
    await delete_msg(call.message)
    await dialog_manager.start(
        CreateOrderSG.enter_city,
        data={
            "promocode_id": callback_data.promocode_id,
            "bonuses_amount": callback_data.bonuses_amount,
        },
    )


async def go_to_order_handler(
    call: types.CallbackQuery,
    callback_data: CallbackData,
    dialog_manager: DialogManager,
):
    await delete_msg(call.message)
    await dialog_manager.start(
        OrderDetailsSG.order_details,
        data={"order_id": callback_data.order_id},
    )


async def resend_stuff_msg(
    call: types.CallbackQuery,
    dialog_manager: DialogManager,
):
    """Повторно отправляем сообщение сотруднику склада через 5 минут"""

    arq_redis: ArqRedis = dialog_manager.middleware_data.get("arqredis")
    await arq_redis.enqueue_job(
        "notify_user",
        _defer_by=timedelta(seconds=10),
        user_tg_id=call.from_user.id,
        text=call.message.text,
        reply_markup=call.message.reply_markup.model_dump_json(),
    )

    await call.answer()
    await delete_msg(call.message)
