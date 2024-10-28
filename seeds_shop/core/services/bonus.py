from seeds_shop.core.models.enums.bonus import OperationType
from seeds_shop.infrastructure.database.models import BonusOperation
from seeds_shop.infrastructure.database.uow import SQLAlchemyUoW


class BonusService:
    def __init__(self, uow: SQLAlchemyUoW):
        self._uow = uow

    async def get_user_bonus_balance(self, user_id: int, days_before_using_bonus: int) -> int:
        """Получаем текущий баланс бонусов юзера"""

        return await self._uow.bonus_reader.get_user_bonus_balance(user_id, days_before_using_bonus)

    async def create_operation(self, user_id: int, operation_type: OperationType, amount: float) -> None:
        bonus_operation = BonusOperation(user_id=user_id, operation_type=operation_type, amount=amount)
        try:
            await self._uow.bonus_repo.create_bonus_operation(bonus_operation)
        except Exception as err:
            await self._uow.rollback()
            raise err

        await self._uow.commit()
