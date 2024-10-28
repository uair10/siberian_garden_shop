from aiogram_dialog import DialogManager

from seeds_shop.core.services import DeliveryZoneService, OrderService, UserService


async def user_info_getter(
    dialog_manager: DialogManager,
    user_service: UserService,
    order_service: OrderService,
    delivery_zone_service: DeliveryZoneService,
    **kwargs,
):
    user_id: int = dialog_manager.event.from_user.id

    user = await user_service.get_user_by_telegram_id(user_id)
    user_orders = await order_service.get_user_orders(user_id)

    delivery_zone = None
    if user.delivery_zone_id:
        delivery_zone = await delivery_zone_service.get_delivery_zone_by_id(user.delivery_zone_id)

    return {
        "user_orders_count": len(user_orders),
        "delivery_zone": delivery_zone,
        "user_id": user_id,
        "reg_date": user.created_at,
        "lang_code": user.lang_code,
    }


async def user_role_getter(dialog_manager: DialogManager, user_service: UserService, **kwargs):
    user_id: int = dialog_manager.event.from_user.id
    user = await user_service.get_user_by_telegram_id(user_id)

    return {"user_role": user.role}
