from seeds_shop.core.models.dto.discount import DiscountDTO
from seeds_shop.infrastructure.database.uow import SQLAlchemyUoW


class DiscountService:
    def __init__(self, uow: SQLAlchemyUoW):
        self._uow = uow

    async def get_discounts_for_shop(self, shop_id: int) -> list[DiscountDTO] | None:
        """Получаем скидки в магазине"""

        return await self._uow.discount_reader.get_discounts_for_shop(shop_id)

    async def get_discount_by_category_and_shop(
        self,
        category_id: int,
        shop_id: int,
        product_count: int,
    ) -> DiscountDTO | None:
        """Получаем скидку по категории и магазину"""

        return await self._uow.discount_reader.get_discount_by_category_and_shop(category_id, shop_id, product_count)
