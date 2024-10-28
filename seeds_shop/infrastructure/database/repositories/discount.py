from sqlalchemy import and_, desc, select

from seeds_shop.core.models.dto.discount import DiscountDTO
from seeds_shop.infrastructure.database.converters.discount import convert_db_model_to_discount_dto
from seeds_shop.infrastructure.database.exception_mapper import exception_mapper
from seeds_shop.infrastructure.database.models import Discount
from seeds_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class DiscountReaderImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_discount_by_category_and_shop(
        self,
        category_id: int,
        shop_id: int,
        product_count: int,
    ) -> DiscountDTO | None:
        """Получаем скидки по категории и магазину"""

        query = (
            select(Discount)
            .where(
                and_(
                    Discount.category_id == category_id,
                    Discount.shop_id == shop_id,
                    Discount.required_quantity <= product_count,
                ),
            )
            .order_by(desc(Discount.required_quantity))
            .limit(1)
        )

        discount: Discount | None = await self._session.scalar(query)

        if not discount:
            return None

        return convert_db_model_to_discount_dto(discount)

    @exception_mapper
    async def get_discounts_for_shop(self, shop_id: int) -> list[DiscountDTO]:
        """Получаем скидки в магазине"""

        query = (
            select(Discount)
            .where(
                and_(
                    Discount.shop_id == shop_id,
                ),
            )
            .order_by(desc(Discount.required_quantity))
        )

        res = await self._session.scalars(query)
        discounts: list[Discount] = list(res)

        return [convert_db_model_to_discount_dto(discount) for discount in discounts]
