from dataclasses import asdict
from decimal import Decimal

from orjson import orjson
from redis.asyncio.client import Redis

from seeds_shop.core.models.dto.cart import CartDTO, CartLineDTO


def default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


class CartManager:
    def __init__(self, redis: Redis):
        self._prefix = "cart"
        self._redis = redis

    async def get_cart(self, user_id: int) -> CartDTO | None:
        key = self._create_key(user_id)
        cart_data = await self._get(key)
        if cart_data:
            return self._deserialize_cart(cart_data)
        return None

    async def set_cart(self, cart: CartDTO) -> None:
        key = self._create_key(cart.user_id)
        cart_data = self._serialize_cart(cart)
        await self._redis.set(key, cart_data)

    def _create_key(self, user_id: int) -> str:
        return f"{self._prefix}:{user_id}"

    @staticmethod
    def _serialize_cart(cart: CartDTO) -> str:
        cart_dict = asdict(cart)
        cart_dict["lines"] = [asdict(product) for product in cart.lines]
        return orjson.dumps(cart_dict, default=default)

    @staticmethod
    def _deserialize_cart(cart_data: str) -> CartDTO:
        cart_dict = orjson.loads(cart_data)
        return CartDTO(
            lines=[CartLineDTO(**product) for product in cart_dict["lines"]],
            user_id=cart_dict.get("user_id"),
            promocode=cart_dict.get("promocode"),
            bonuses_amount=cart_dict.get("bonuses_amount"),
            total_amount=cart_dict.get("total_amount"),
        )

    async def _get(self, key: str, encoding: str = "utf-8") -> str | None:
        value = await self._redis.get(key)
        return value.decode(encoding) if value else None
