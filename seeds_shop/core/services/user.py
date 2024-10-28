import logging

from seeds_shop.core.models.dto.user import UserDTO
from seeds_shop.core.models.enums.user import LangCode, UserRole
from seeds_shop.infrastructure.database.models import Review, User
from seeds_shop.infrastructure.database.uow import SQLAlchemyUoW

logger = logging.getLogger(__name__)


class UserService:
    """Сервис для работы с пользователями"""

    def __init__(self, uow: SQLAlchemyUoW):
        self._uow = uow

    async def get_user_by_id(self, user_id: int) -> UserDTO:
        """Получаем пользователя по id"""

        return await self._uow.user_reader.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str) -> UserDTO:
        """Получаем пользователя по username"""

        return await self._uow.user_reader.get_user_by_username(username)

    async def get_user_by_telegram_id(self, user_tg_id: int) -> UserDTO:
        """Получаем пользователя по telegram id"""

        return await self._uow.user_reader.get_user_by_tg_id(user_tg_id)

    async def get_users_by_role_and_shop_id(self, role: UserRole, shop_id: int, delivery_zone_id: int | None = None):
        """Получаем пользователей с ролью в магазине"""

        return await self._uow.user_reader.get_users_by_role_and_shop_id(role, shop_id, delivery_zone_id)

    async def get_all_users(self) -> list[UserDTO]:
        """Получаем всех пользователей"""

        return await self._uow.user_reader.get_users()

    async def change_user_lang(self, user_tg_id: int, lang_code: LangCode) -> None:
        """Изменяем язык пользователя"""

        user: User = await self._uow.user_repo.acquire_user_by_tg_id(user_tg_id)
        user.lang_code = lang_code

        await self._uow.user_repo.update_user(user)

        await self._uow.commit()

    async def create_user(self, telegram_id: int, username: str, delivery_zone_id: int = 1) -> None:
        """Создаем пользователя"""

        user = User(telegram_id=telegram_id, username=username, delivery_zone_id=delivery_zone_id)
        try:
            await self._uow.user_repo.create_user(user)
        except Exception as err:
            await self._uow.rollback()
            raise err

        await self._uow.commit()

    async def create_user_review(self, user_tg_id: int, review_text: str) -> None:
        """Добавляем отзыв пользователя"""

        user: User = await self._uow.user_repo.acquire_user_by_tg_id(user_tg_id)
        review = Review(user_id=user.id, review_text=review_text)

        try:
            await self._uow.review_repo.create_review(review)
        except Exception as err:
            await self._uow.rollback()
            raise err

        await self._uow.commit()
