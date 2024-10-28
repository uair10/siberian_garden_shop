import os.path

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from seeds_shop.core.constants import ASSETS_FOLDER
from seeds_shop.core.services import PaymentMethodService
from seeds_shop.tg_bot.services.locale import Locale


async def payment_methods_getter(
    dialog_manager: DialogManager,
    locale: Locale,
    payment_method_service: PaymentMethodService,
    **kwargs,
):
    payment_methods = await payment_method_service.get_payment_methods()
    for payment_method in payment_methods:
        payment_method.currency = locale.get(payment_method.currency.value)  # type: ignore

    return {"payment_methods": payment_methods}


async def payment_method_getter(
    dialog_manager: DialogManager,
    payment_method_service: PaymentMethodService,
    **kwargs,
):
    payment_method_id = dialog_manager.dialog_data.get("payment_method_id", 1)
    payment_method = await payment_method_service.get_payment_method_by_id(int(payment_method_id))
    payment_image = None
    try:
        file_path = os.path.join(ASSETS_FOLDER, payment_method.payment_image_path)
        if os.path.isfile(file_path):
            payment_image = MediaAttachment(
                path=file_path,
                type=ContentType.PHOTO,
            )
    except TypeError:
        pass

    return {
        "currency": payment_method.currency_symbol.value,
        "payment_address": payment_method.payment_address,
        "payment_image": payment_image,
    }
