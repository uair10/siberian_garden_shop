from decimal import Decimal
from typing import Annotated

from arq import ArqRedis, create_pool
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from seeds_shop.api.controllers.requests.cart import WebAppCart
from seeds_shop.core.config import Settings
from seeds_shop.core.models.dto.cart import CartDTO, CartLineDTO
from seeds_shop.infrastructure.database.redis import CartManager

cart_router = APIRouter(prefix="/cart", tags=["cart"])


@cart_router.post("/create")
@inject
async def update_cart_products(
    cart: WebAppCart,
    user_tg_id: int,
    config: Annotated[Settings, FromDishka()],
    cart_manager: Annotated[CartManager, FromDishka()],
):
    """Создаем корзину и перекидываем ее в бота"""

    arq_redis: ArqRedis = await create_pool(config.redis.pool_settings)

    cart_lines = [
        CartLineDTO(
            title=item.title,
            product_id=item.id,
            quantity=item.quantity,
            final_unit_price=item.discounted_price,
        )
        for item in cart.items
    ]
    cart = CartDTO(
        lines=cart_lines,
        user_id=user_tg_id,
        promocode=cart.promocode,
        bonuses_amount=cart.bonusesAmount,
        total_amount=Decimal(cart.totalAmount),
    )

    await cart_manager.set_cart(cart)
    # TODO Добавить обработку ошибки, если введенное число бонусов больше, чем бонусов у юзера

    await arq_redis.enqueue_job("send_cart_confirmation_msg", user_tg_id=user_tg_id, cart=cart)
