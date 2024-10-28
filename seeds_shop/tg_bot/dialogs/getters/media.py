import os

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from seeds_shop.core.constants import INVOICES_FOLDER
from seeds_shop.core.services import OrderService


async def invoice_screenshot_getter(dialog_manager: DialogManager, order_service: OrderService, **kwargs):
    """Получаем скриншот об оплате заказа"""

    order_id: int = dialog_manager.start_data.get("order_id")

    order = await order_service.get_order_by_id(order_id)

    invoice_file = None
    try:
        file_path = os.path.join(INVOICES_FOLDER, order.invoice_screenshot_path)
        if os.path.isfile(file_path):
            invoice_file = MediaAttachment(
                path=file_path,
                type=ContentType.DOCUMENT,
            )
    except TypeError:
        pass

    return {"invoice_screenshot": invoice_file}
