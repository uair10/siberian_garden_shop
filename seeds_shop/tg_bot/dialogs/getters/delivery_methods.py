from aiogram_dialog import DialogManager

from seeds_shop.core.services.delivery_method import DeliveryMethodService


async def delivery_methods_getter(
    dialog_manager: DialogManager, delivery_method_service: DeliveryMethodService, **kwargs
):
    delivery_methods = await delivery_method_service.get_delivery_methods_by_city(
        dialog_manager.dialog_data.get("city_id")
    )

    return {
        "delivery_methods": delivery_methods,
    }


async def delivery_method_getter(
    dialog_manager: DialogManager, delivery_method_service: DeliveryMethodService, **kwargs
):
    delivery_method = await delivery_method_service.get_delivery_method_by_id(
        dialog_manager.dialog_data.get("delivery_method_id")
    )

    return {"accompanying_message": delivery_method.accompanying_message}
