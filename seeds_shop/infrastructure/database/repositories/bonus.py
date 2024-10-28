from datetime import timedelta

from sqlalchemy import and_, func, select
from sqlalchemy.exc import DBAPIError, IntegrityError

from seeds_shop.core.exceptions.common import RepoError
from seeds_shop.core.models.enums.bonus import OperationType
from seeds_shop.core.utils.date_time import get_date_time
from seeds_shop.infrastructure.database.exception_mapper import exception_mapper
from seeds_shop.infrastructure.database.models.bonus_operation import BonusOperation
from seeds_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class BonusReaderImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_user_bonus_balance(self, user_id: int, days_before_using_bonus: int) -> int:
        """
        Получаем текущий баланс бонусов юзера
        :param user_id: Id юзера
        :param days_before_using_bonus: Кол-во дней, по прошествии которого можно использовать бонус
        """

        cur_date = get_date_time()

        min_date_to_use_bonus = cur_date - timedelta(days=days_before_using_bonus)

        query = select(func.sum(BonusOperation.amount)).filter(
            and_(
                BonusOperation.operation_type == OperationType.ACCRUAL,
                BonusOperation.user_id == user_id,
                BonusOperation.created_at <= min_date_to_use_bonus if days_before_using_bonus > 0 else True,
            ),
        )
        accrual_amount = await self._session.scalar(query) or 0

        query = select(func.sum(BonusOperation.amount)).filter(
            BonusOperation.operation_type == OperationType.DEDUCTION,
            BonusOperation.user_id == user_id,
        )
        deduction_amount = await self._session.scalar(query) or 0

        current_balance = accrual_amount - deduction_amount
        return max(current_balance, 0)


class BonusRepoImpl(SQLAlchemyRepo):
    @exception_mapper
    async def create_bonus_operation(self, bonus_operation: BonusOperation):
        self._session.add(bonus_operation)
        try:
            await self._session.flush((bonus_operation,))
        except IntegrityError as err:
            self._parse_error(err)

    @staticmethod
    def _parse_error(err: DBAPIError) -> None:
        raise RepoError from err
