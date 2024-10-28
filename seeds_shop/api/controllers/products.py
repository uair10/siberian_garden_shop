from typing import Annotated

from cashews import cache
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette import status

from seeds_shop.api.controllers.requests.cart import CartItem, WebAppCart
from seeds_shop.core.models.dto.category import CategoryDTO
from seeds_shop.core.models.dto.product import ProductDTO, ProductWithQuantityDTO
from seeds_shop.core.price_calculation import calculate_product_discounted_price
from seeds_shop.core.services import (
    BotSettingsService,
    DiscountService,
    ProductService,
    PromocodeService,
    ShopService,
    UserService,
)

products_router = APIRouter(prefix="/products", tags=["products"])


@products_router.get(
    "/{product_id}",
    responses={
        status.HTTP_200_OK: {"model": ProductDTO},
    },
)
@cache(ttl="1m")
@inject
async def get_product(
    product_id: int,
    user_tg_id: int,
    products_service: Annotated[ProductService, FromDishka()],
    user_service: Annotated[UserService, FromDishka()],
    shop_service: Annotated[ShopService, FromDishka()],
):
    user = await user_service.get_user_by_telegram_id(user_tg_id)
    product = await products_service.get_product_by_id(product_id)
    shop = await shop_service.get_shop_by_delivery_zone_id(user.delivery_zone_id)

    available_quantity = await products_service.get_product_available_quantity(
        shop.id, user.delivery_zone_id, product.id
    )
    product.available_quantity = available_quantity

    return product


@products_router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": list[ProductDTO]},
    },
    description="Return all categories and products",
)
@cache(ttl="1m", key="user_products:{user_tg_id}")
@inject
async def get_products_and_categories(
    user_tg_id: int,
    products_service: Annotated[ProductService, FromDishka()],
    user_service: Annotated[UserService, FromDishka()],
    shop_service: Annotated[ShopService, FromDishka()],
) -> tuple[list[ProductDTO], list[CategoryDTO]]:
    user = await user_service.get_user_by_telegram_id(user_tg_id)
    products, categories = await products_service.get_products_and_categories(user.delivery_zone_id)
    shop = await shop_service.get_shop_by_delivery_zone_id(user.delivery_zone_id)
    for product in products:
        available_quantity = await products_service.get_product_available_quantity(
            shop.id, user.delivery_zone_id, product.id
        )
        product.available_quantity = available_quantity

    return products, categories


@products_router.post(
    "/calculate_discount/",
    description="Calculate cart items discounts",
    response_model=list[CartItem],
)
@inject
async def calculate_cart_discount(
    cart: WebAppCart,
    products_service: Annotated[ProductService, FromDishka()],
    user_service: Annotated[UserService, FromDishka()],
    shop_service: Annotated[ShopService, FromDishka()],
    promocode_service: Annotated[PromocodeService, FromDishka()],
    discount_service: Annotated[DiscountService, FromDishka()],
    bot_settings_service: Annotated[BotSettingsService, FromDishka()],
    user_tg_id: int | None = None,
    table_number: int | None = None,
) -> list[CartItem]:
    user = await user_service.get_user_by_telegram_id(user_tg_id)
    if not user_tg_id:
        user = await user_service.get_user_by_username(f"Table {table_number}")

    cart_items = cart.items
    shop = await shop_service.get_shop_by_delivery_zone_id(user.delivery_zone_id)
    discounts = await discount_service.get_discounts_for_shop(shop.id)
    bot_settings = await bot_settings_service.get_bot_settings()

    promocode = await promocode_service.get_promocode_by_name(cart.promocode)

    products = [await products_service.get_product_by_id(item.id) for item in cart_items]
    products_with_quantity = [
        ProductWithQuantityDTO(product=product, quantity=item.quantity)
        for item in cart_items
        for product in products
        if item.id == product.id
    ]
    for product, item in zip(
        sorted(products, key=lambda x: x.id), sorted(cart_items, key=lambda x: x.id), strict=False
    ):
        item.discounted_price = float(
            calculate_product_discounted_price(
                product,
                item.quantity,
                products_with_quantity,
                bot_settings.maximum_bonus_discount_percent,
                discounts,
                bonuses_amount=cart.bonusesAmount,
                promocode_percent=promocode.amount if promocode else None,
            ),
        )
        item.images = product.images  # TODO Переделать
        item.available_quantity = await products_service.get_product_available_quantity(
            shop.id, user.delivery_zone_id, item.id
        )

    return cart_items
