from sqlalchemy import and_, select
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm import joinedload

from seeds_shop.core.exceptions.common import RepoError
from seeds_shop.core.models.dto.category import CategoryDTO
from seeds_shop.core.models.dto.product import ProductDTO
from seeds_shop.infrastructure.database.converters.category import convert_db_model_to_category_dto
from seeds_shop.infrastructure.database.converters.product import (
    convert_db_model_to_product_dto,
    convert_db_model_to_product_with_params_dto,
)
from seeds_shop.infrastructure.database.exception_mapper import exception_mapper
from seeds_shop.infrastructure.database.models import Category, Product, Shop, Stock
from seeds_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class ProductReaderImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_product_by_id(self, product_id: int) -> ProductDTO | None:
        """Получаем товар по id"""

        product: Product | None = await self._session.scalar(
            select(Product)
            .where(
                Product.id == product_id,
            )
            .options(joinedload(Product.feelings), joinedload(Product.genetics), joinedload(Product.images)),
        )
        if not product:
            return None

        return convert_db_model_to_product_with_params_dto(product)

    @exception_mapper
    async def get_product_by_sku(self, product_sku: str) -> ProductDTO | None:
        """Получаем товар по sku"""

        product: Product | None = await self._session.scalar(
            select(Product)
            .where(
                Product.sku == product_sku,
            )
            .options(joinedload(Product.feelings), joinedload(Product.genetics), joinedload(Product.images)),
        )
        if not product:
            return None

        return convert_db_model_to_product_with_params_dto(product)

    @exception_mapper
    async def get_category_by_id(self, category_id: int) -> CategoryDTO | None:
        """Получаем товар по sku"""

        category: Category | None = await self._session.scalar(
            select(Category).where(
                Category.id == category_id,
            )
        )
        if not category:
            return None

        return convert_db_model_to_category_dto(category)

    @exception_mapper
    async def get_products_and_categories(self, delivery_zone_id: int) -> tuple[list[ProductDTO], list[CategoryDTO]]:
        """Получаем товары и категории в зоне доставки"""

        query = (
            select(Product)
            .join(Product.stock)
            .filter(
                and_(
                    Stock.delivery_zone_id == delivery_zone_id,
                    Stock.available_quantity > 0,
                ),
            )
            .options(joinedload(Product.category), joinedload(Product.images))
        )
        res = await self._session.scalars(query)
        products: list[Product] = list(res.unique())
        products.sort(key=lambda x: x.webapp_position, reverse=True)

        products_dtos = [convert_db_model_to_product_dto(product) for product in products]

        categories: list[Category] = list(set([product.category for product in products]))
        categories.sort(key=lambda x: x.position_number)
        categories_dtos = [convert_db_model_to_category_dto(category) for category in categories]

        return products_dtos, categories_dtos

    @exception_mapper
    async def get_product_stock_amount(self, shop_id: int, delivery_zone_id: int, product_id: int) -> int:
        """Получаем остатки товара в магазине"""

        query = (
            select(Stock)
            .join(Stock.shop)
            .filter(
                and_(
                    Shop.id == shop_id,
                    Stock.delivery_zone_id == delivery_zone_id,
                    Stock.product_id == product_id,
                )
            )
        )

        stock: Stock | None = await self._session.scalar(query)

        if not stock:
            return 0

        return stock.available_quantity


class ProductRepoImpl(SQLAlchemyRepo):
    @exception_mapper
    async def acquire_product_by_id(self, product_id: int) -> Product | None:
        """Получаем товар по id"""

        product: Product | None = await self._session.scalar(
            select(Product).where(
                Product.id == product_id,
            ),
        )
        if not product:
            return None

        return product

    @exception_mapper
    async def acquire_product_stock_in_shop(self, shop_id: int, delivery_zone_id: int, product_id: int) -> Stock | None:
        """Получаем остатки товара в магазине"""

        query = (
            select(Stock)
            .join(Stock.shop)
            .filter(
                and_(
                    Shop.id == shop_id,
                    Stock.product_id == product_id,
                    Stock.delivery_zone_id == delivery_zone_id,
                ),
            )
        )

        stock: Stock | None = await self._session.scalar(query)

        if not stock:
            return None

        return stock

    @exception_mapper
    async def update_product(self, product: Product):
        try:
            await self._session.merge(product)
        except IntegrityError as err:
            self._parse_error(err)

    @exception_mapper
    async def update_stock(self, stock: Stock):
        """Обновляем остатки товара"""

        try:
            await self._session.merge(stock)
        except IntegrityError as err:
            self._parse_error(err)

    @staticmethod
    def _parse_error(err: DBAPIError) -> None:
        raise RepoError from err
