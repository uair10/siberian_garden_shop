import logging

from seeds_shop.core.models.dto.category import CategoryDTO
from seeds_shop.core.models.dto.product import ProductDTO
from seeds_shop.infrastructure.database.models import Product, Stock
from seeds_shop.infrastructure.database.uow import SQLAlchemyUoW

logger = logging.getLogger(__name__)


class ProductService:
    def __init__(self, uow: SQLAlchemyUoW):
        self._uow = uow

    async def get_product_by_id(self, product_id: int) -> ProductDTO | None:
        """Получаем товар по id"""

        return await self._uow.product_reader.get_product_by_id(product_id)

    async def get_product_by_sku(self, product_sku: str) -> ProductDTO | None:
        """Получаем товар по sku"""

        return await self._uow.product_reader.get_product_by_sku(product_sku)

    async def get_products_and_categories(self, delivery_zone_id: int) -> tuple[list[ProductDTO], list[CategoryDTO]]:
        """Получаем товары и категории в зоне доставки"""

        return await self._uow.product_reader.get_products_and_categories(delivery_zone_id)

    async def get_category_by_id(self, category_id: int) -> CategoryDTO | None:
        return await self._uow.product_reader.get_category_by_id(category_id)

    async def get_product_available_quantity(self, shop_id: int, delivery_zone_id: int, product_id: int) -> int:
        """Получаем доступное кол-во товара в магазине в зоне доставки"""

        return await self._uow.product_reader.get_product_stock_amount(shop_id, delivery_zone_id, product_id)

    async def increase_product_sold_count(self, product_id: int, quantity: int) -> None:
        """Увеличиваем число продаж товара"""

        product: Product = await self._uow.product_repo.acquire_product_by_id(product_id)
        product.sold_count += quantity

        await self._uow.product_repo.update_product(product)

        await self._uow.commit()

    async def increase_product_available_quantity(
        self, shop_id: int, delivery_zone_id: int, product_id: int, quantity: int
    ) -> None:
        """Увеличиваем остаток по товару в магазине"""

        stock: Stock = await self._uow.product_repo.acquire_product_stock_in_shop(shop_id, delivery_zone_id, product_id)
        stock.available_quantity += quantity

        await self._uow.product_repo.update_stock(stock)

        await self._uow.commit()

        logger.info(
            f"Stock for product {product_id} in shop {shop_id} was updated. New available quantity: {stock.available_quantity}",
        )
