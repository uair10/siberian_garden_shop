from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Form
from fluentogram import TranslatorRunner

from seeds_shop.core.services import OrderService, PromocodeService, UserService
from seeds_shop.tg_bot.services.locale import Localizator

promocode_router = APIRouter(prefix="/promocode", tags=["promocode"])


@promocode_router.post("/check")
@inject
async def check_promocode(
    promocode_name: Annotated[str, Form()],
    user_tg_id: Annotated[int, Form()],
    user_service: Annotated[UserService, FromDishka()],
    promocode_service: Annotated[PromocodeService, FromDishka()],
    order_service: Annotated[OrderService, FromDishka()],
    localizator: Annotated[Localizator, FromDishka()],
):
    user = await user_service.get_user_by_telegram_id(user_tg_id)
    locale: TranslatorRunner = localizator.get_by_locale(user.lang_code)

    promocode = await promocode_service.get_promocode_by_name(promocode_name)

    if not promocode:
        return {"success": False, "message": locale.get("wrong-promocode")}

    if promocode.uses_number >= promocode.limit != 0:
        return {
            "success": False,
            "message": locale.get("promocode-usage-limit-reached"),
        }

    if await order_service.get_order_with_promocode(user_tg_id, promocode.id) and not promocode.reusable:
        # Запрещаем одному и тому же юзеру использовать один промо в разных заказах
        return {"success": False, "message": locale.get("promocode-already-used")}

    return {
        "success": True,
        "message": locale.get("promocode-activated", discount_percent=promocode.amount),
        "promocode_name": promocode_name,
        "promocode_id": promocode.id,
        "discount_value": promocode.amount,
    }
