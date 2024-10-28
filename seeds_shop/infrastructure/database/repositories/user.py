import logging

from sqlalchemy import and_, select
from sqlalchemy.exc import DBAPIError, IntegrityError

from seeds_shop.core.exceptions.common import RepoError
from seeds_shop.core.exceptions.user import (
    UserIdAlreadyExist,
    UserIdNotExist,
    UserNameNotExist,
    UserTgIdAlreadyExist,
    UserTgIdNotExist,
)
from seeds_shop.core.models.dto.user import UserDTO
from seeds_shop.core.models.enums.user import UserRole
from seeds_shop.infrastructure.database.converters.user import convert_db_model_to_user_dto
from seeds_shop.infrastructure.database.exception_mapper import exception_mapper
from seeds_shop.infrastructure.database.models import User
from seeds_shop.infrastructure.database.repositories.base import SQLAlchemyRepo

logger = logging.getLogger(__name__)


class UserReaderImpl(SQLAlchemyRepo):
    @exception_mapper
    async def get_user_by_id(self, user_id: int) -> UserDTO:
        """Получаем пользователя по id"""

        user: User | None = await self._session.scalar(
            select(User).where(
                User.id == user_id,
            )
        )
        if not user:
            raise UserIdNotExist

        return convert_db_model_to_user_dto(user)

    @exception_mapper
    async def get_user_by_username(self, username: int) -> UserDTO:
        """Получаем пользователя по username"""

        user: User | None = await self._session.scalar(
            select(User).where(
                User.username == username,
            )
        )
        if not user:
            raise UserNameNotExist

        return convert_db_model_to_user_dto(user)

    @exception_mapper
    async def get_user_by_tg_id(self, user_tg_id: int) -> User | UserDTO:
        """Получаем пользователя по telegram id"""

        user: User | None = await self._session.scalar(
            select(User).where(
                User.telegram_id == user_tg_id,
            ),
        )
        if not user:
            raise UserTgIdNotExist

        return convert_db_model_to_user_dto(user)

    @exception_mapper
    async def get_users(self) -> list[UserDTO]:
        """Получаем пользователей"""

        res = await self._session.scalars(select(User))
        users: list[User] = list(res)

        return [convert_db_model_to_user_dto(user) for user in users]

    @exception_mapper
    async def get_users_by_role_and_shop_id(
        self, role: UserRole, shop_id: int, delivery_zone_id: int | None = None
    ) -> list[UserDTO]:
        """Получаем пользователей с ролью в магазине"""

        query = select(User).where(
            and_(
                User.role == role,
                User.shop_id == shop_id,
            )
        )
        if delivery_zone_id:
            query = query.where(User.working_delivery_zone_id == delivery_zone_id)

        res = await self._session.scalars(query)
        users: list[User] = list(res)

        return [convert_db_model_to_user_dto(user) for user in users]


class UserRepoImpl(SQLAlchemyRepo):
    @exception_mapper
    async def acquire_user_by_id(self, user_id: int) -> User | UserDTO:
        """Получаем пользователя по id"""

        user: User | None = await self._session.scalar(
            select(User).where(
                User.id == user_id,
            ),
        )
        if not user:
            raise UserIdNotExist

        return user

    @exception_mapper
    async def acquire_user_by_tg_id(self, user_tg_id: int) -> User | UserDTO:
        """Получаем пользователя по telegram id"""

        user: User | None = await self._session.scalar(
            select(User).where(
                User.telegram_id == user_tg_id,
            ),
        )
        if not user:
            raise UserTgIdNotExist

        return user

    @exception_mapper
    async def create_user(self, user: User) -> None:
        """Создаем пользователя"""

        self._session.add(user)
        try:
            await self._session.flush((user,))
        except IntegrityError as err:
            self._parse_error(err)

    @exception_mapper
    async def update_user(self, user: User) -> None:
        """Обновляем пользователя"""

        try:
            await self._session.merge(user)
        except IntegrityError as err:
            self._parse_error(err)

    @staticmethod
    def _parse_error(err: DBAPIError) -> None:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "pk_user":
                raise UserIdAlreadyExist from err
            case "uq_user_telegram_id":
                raise UserTgIdAlreadyExist from err
            case _:
                raise RepoError from err
