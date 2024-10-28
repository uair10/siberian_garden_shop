from typing import AsyncIterable

from dishka import Provider, Scope, provide
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from seeds_shop.core.config import DbConfig, RedisConfig
from seeds_shop.core.services import (
    BonusService,
    BotSettingsService,
    DeliveryZoneService,
    DiscountService,
    OrderService,
    PaymentMethodService,
    ProductService,
    PromocodeService,
    ShopService,
    StatsService,
    TicketService,
    UserService,
)
from seeds_shop.core.services.delivery_method import DeliveryMethodService
from seeds_shop.infrastructure.database.factory import build_sa_engine, build_sa_session_factory, create_redis
from seeds_shop.infrastructure.database.redis import CartManager, TelegramMessageStorage
from seeds_shop.infrastructure.database.uow import SQLAlchemyUoW
from seeds_shop.infrastructure.database.uow.uow import build_uow


class DbProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_engine(self, db_config: DbConfig) -> AsyncIterable[AsyncEngine]:
        engine = build_sa_engine(db_config)
        yield engine
        await engine.dispose(True)

    @provide
    def get_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return build_sa_session_factory(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, pool: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with pool() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_uow(self, session: AsyncSession) -> SQLAlchemyUoW:
        return build_uow(session=session)

    @provide(scope=Scope.REQUEST)
    def get_user_service(self, uow: SQLAlchemyUoW) -> UserService:
        return UserService(uow=uow)

    @provide(scope=Scope.REQUEST)
    def get_product_service(self, uow: SQLAlchemyUoW) -> ProductService:
        return ProductService(uow=uow)

    @provide(scope=Scope.REQUEST)
    def get_shop_service(self, uow: SQLAlchemyUoW) -> ShopService:
        return ShopService(uow=uow)

    @provide(scope=Scope.REQUEST)
    def get_discount_service(self, uow: SQLAlchemyUoW) -> DiscountService:
        return DiscountService(uow=uow)

    @provide(scope=Scope.REQUEST)
    def get_order_service(self, uow: SQLAlchemyUoW) -> OrderService:
        return OrderService(uow=uow)

    @provide(scope=Scope.REQUEST)
    def get_promocode_service(self, uow: SQLAlchemyUoW) -> PromocodeService:
        return PromocodeService(uow=uow)

    @provide(scope=Scope.REQUEST)
    def get_bot_settings_service(self, uow: SQLAlchemyUoW) -> BotSettingsService:
        return BotSettingsService(uow=uow)

    @provide(scope=Scope.REQUEST)
    def get_bonus_service(self, uow: SQLAlchemyUoW) -> BonusService:
        return BonusService(uow=uow)

    @provide(scope=Scope.REQUEST)
    def get_ticket_service(self, uow: SQLAlchemyUoW) -> TicketService:
        return TicketService(uow=uow)

    @provide(scope=Scope.REQUEST)
    def get_stats_service(self, uow: SQLAlchemyUoW) -> StatsService:
        return StatsService(uow=uow)

    @provide(scope=Scope.REQUEST)
    def get_payment_method_service(self, uow: SQLAlchemyUoW) -> PaymentMethodService:
        return PaymentMethodService(uow=uow)

    @provide(scope=Scope.REQUEST)
    def get_delivery_method_service(self, uow: SQLAlchemyUoW) -> DeliveryMethodService:
        return DeliveryMethodService(uow=uow)

    @provide(scope=Scope.REQUEST)
    def get_delivery_zone_service(self, uow: SQLAlchemyUoW) -> DeliveryZoneService:
        return DeliveryZoneService(uow=uow)

    @provide(scope=Scope.REQUEST)
    def get_cart_manager(self, redis: Redis) -> CartManager:
        return CartManager(redis=redis)

    @provide(scope=Scope.REQUEST)
    def get_telegram_message_storage(self, redis: Redis) -> TelegramMessageStorage:
        return TelegramMessageStorage(redis=redis)


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_redis(self, config: RedisConfig) -> AsyncIterable[Redis]:
        async with create_redis(config) as redis:
            yield redis
