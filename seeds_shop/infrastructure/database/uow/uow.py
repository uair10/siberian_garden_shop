from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from seeds_shop.infrastructure.database import repositories as repo
from seeds_shop.infrastructure.database.uow.base import SQLAlchemyBaseUoW


@dataclass(frozen=True)
class SQLAlchemyUoW(SQLAlchemyBaseUoW):
    session: AsyncSession
    user_reader: repo.UserReaderImpl
    user_repo: repo.UserRepoImpl
    order_reader: repo.OrderReaderImpl
    order_repo: repo.OrderRepoImpl
    delivery_zone_reader: repo.DeliveryZoneReaderImpl
    product_reader: repo.ProductReaderImpl
    product_repo: repo.ProductRepoImpl
    payment_method_reader: repo.PaymentMethodReaderImpl
    shop_reader: repo.ShopReaderImpl
    ticket_reader: repo.TicketReaderImpl
    ticket_repo: repo.TicketRepoImpl
    stats_repo: repo.StatsRepoImpl
    review_repo: repo.ReviewRepoImpl
    discount_reader: repo.DiscountReaderImpl
    promocode_reader: repo.PromocodeReaderImpl
    promocode_repo: repo.PromocodeRepoImpl
    bot_settings_reader: repo.BotSettingsReaderImpl
    bot_settings_repo: repo.BotSettingsRepoImpl
    bonus_reader: repo.BonusReaderImpl
    bonus_repo: repo.BonusRepoImpl
    delivery_method_reader: repo.DeliveryMethodReaderImpl


def build_uow(session: AsyncSession):
    return SQLAlchemyUoW(
        session=session,
        user_reader=repo.UserReaderImpl(session),
        user_repo=repo.UserRepoImpl(session),
        order_reader=repo.OrderReaderImpl(session),
        order_repo=repo.OrderRepoImpl(session),
        delivery_zone_reader=repo.DeliveryZoneReaderImpl(session),
        product_reader=repo.ProductReaderImpl(session),
        product_repo=repo.ProductRepoImpl(session),
        payment_method_reader=repo.PaymentMethodReaderImpl(session),
        shop_reader=repo.ShopReaderImpl(session),
        ticket_reader=repo.TicketReaderImpl(session),
        ticket_repo=repo.TicketRepoImpl(session),
        stats_repo=repo.StatsRepoImpl(session),
        review_repo=repo.ReviewRepoImpl(session),
        discount_reader=repo.DiscountReaderImpl(session),
        promocode_reader=repo.PromocodeReaderImpl(session),
        promocode_repo=repo.PromocodeRepoImpl(session),
        bot_settings_reader=repo.BotSettingsReaderImpl(session),
        bot_settings_repo=repo.BotSettingsRepoImpl(session),
        bonus_reader=repo.BonusReaderImpl(session),
        bonus_repo=repo.BonusRepoImpl(session),
        delivery_method_reader=repo.DeliveryMethodReaderImpl(session),
    )
