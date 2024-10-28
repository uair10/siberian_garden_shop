from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from arq import ArqRedis
from dishka import AsyncContainer

from seeds_shop.core.config import Settings
from seeds_shop.core.services import (
    BonusService,
    BotSettingsService,
    DeliveryZoneService,
    DiscountService,
    OrderService,
    PaymentMethodService,
    ProductService,
    PromocodeService,
    ShopService,
    StatsService,
    TicketService,
    UserService,
)
from seeds_shop.core.services.delivery_method import DeliveryMethodService
from seeds_shop.infrastructure.database.redis import CartManager
from seeds_shop.infrastructure.database.uow import SQLAlchemyUoW
from seeds_shop.tg_bot.services.locale import Localizator


class InitMiddleware(BaseMiddleware):
    def __init__(
        self,
        container: AsyncContainer,
    ) -> None:
        self.container = container

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ):
        data["config"] = await self.container.get(Settings)
        data["localizator"] = await self.container.get(Localizator)
        data["arqredis"] = await self.container.get(ArqRedis)

        async with self.container() as request_container:
            uow = await request_container.get(SQLAlchemyUoW)
            data["uow"] = uow
            data["user_service"] = await request_container.get(UserService)
            data["order_service"] = await request_container.get(OrderService)
            data["delivery_zone_service"] = await request_container.get(DeliveryZoneService)
            data["product_service"] = await request_container.get(ProductService)
            data["payment_method_service"] = await request_container.get(PaymentMethodService)
            data["delivery_method_service"] = await request_container.get(DeliveryMethodService)
            data["shop_service"] = await request_container.get(ShopService)
            data["ticket_service"] = await request_container.get(TicketService)
            data["stats_service"] = await request_container.get(StatsService)
            data["discount_service"] = await request_container.get(DiscountService)
            data["promocode_service"] = await request_container.get(PromocodeService)
            data["bot_settings_service"] = await request_container.get(BotSettingsService)
            data["bonus_service"] = await request_container.get(BonusService)
            data["cart_manager"] = await request_container.get(CartManager)
            result = await handler(event, data)

        return result
