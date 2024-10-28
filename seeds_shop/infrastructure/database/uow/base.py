from dataclasses import dataclass

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from seeds_shop.core.exceptions.common import CommitError, RollbackError


@dataclass(frozen=True)
class SQLAlchemyBaseUoW:
    session: AsyncSession

    async def commit(self) -> None:
        """
        Сохранение изменений в бд
        """
        try:
            await self.session.commit()
        except SQLAlchemyError as err:
            raise CommitError() from err

    async def rollback(self) -> None:
        """
        Откат изменений в бд
        """
        try:
            await self.session.rollback()
        except SQLAlchemyError as err:
            raise RollbackError() from err
