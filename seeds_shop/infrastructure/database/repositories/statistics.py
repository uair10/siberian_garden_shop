import datetime

from sqlalchemy import insert, select
from sqlalchemy.exc import DBAPIError, IntegrityError

from seeds_shop.core.exceptions.stats import StatsForDateAlreadyExists
from seeds_shop.infrastructure.database.exception_mapper import exception_mapper
from seeds_shop.infrastructure.database.models import Statistics
from seeds_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class StatsRepoImpl(SQLAlchemyRepo):
    @exception_mapper
    async def acquire_stats_by_date(self, date: datetime.date) -> Statistics | None:
        stats: Statistics | None = await self._session.scalar(select(Statistics).where(Statistics.date == date))

        if not stats:
            return None

        return stats

    @exception_mapper
    async def create_stats(
        self,
        date: datetime.date,
        products_purchased: int,
        orders_created: int,
        users_registered: int,
        tickets_opened: int,
    ) -> None:
        await self._session.execute(
            insert(Statistics).values(
                date=date,
                products_purchased=products_purchased,
                orders_created=orders_created,
                users_registered=users_registered,
                tickets_opened=tickets_opened,
            ),
        )

    @exception_mapper
    async def update_stats(self, stats: Statistics):
        try:
            await self._session.merge(stats)
        except IntegrityError as err:
            self._parse_error(err)

    @staticmethod
    def _parse_error(err: DBAPIError) -> None:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "uq_stats_date":
                raise StatsForDateAlreadyExists
