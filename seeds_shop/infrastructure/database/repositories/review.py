from sqlalchemy.exc import DBAPIError, IntegrityError

from seeds_shop.core.exceptions.common import RepoError
from seeds_shop.infrastructure.database.exception_mapper import exception_mapper
from seeds_shop.infrastructure.database.models import Review
from seeds_shop.infrastructure.database.repositories.base import SQLAlchemyRepo


class ReviewRepoImpl(SQLAlchemyRepo):
    @exception_mapper
    async def create_review(self, review: Review):
        self._session.add(review)
        try:
            await self._session.flush((review,))
        except IntegrityError as err:
            self._parse_error(err)

    @exception_mapper
    async def update_review(self, review: Review) -> None:
        try:
            await self._session.merge(review)
        except IntegrityError as err:
            self._parse_error(err)

    @staticmethod
    def _parse_error(err: DBAPIError) -> None:
        raise RepoError from err
