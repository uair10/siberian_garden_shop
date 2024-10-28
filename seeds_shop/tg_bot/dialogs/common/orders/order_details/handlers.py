import logging

from aiogram import Bot, types
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from seeds_shop.core.config import Settings
from seeds_shop.core.models.enums.bonus import OperationType
from seeds_shop.core.models.enums.order import OrderStatus
from seeds_shop.core.models.enums.user import UserRole
from seeds_shop.core.price_calculation import calculate_bonuses_for_order
from seeds_shop.core.services import (
    BonusService,
    BotSettingsService,
    OrderService,
    PaymentMethodService,
    ShopService,
    UserService,
)
from seeds_shop.tg_bot.keyboards.inline import after_order_kb, order_shipping_kb
from seeds_shop.tg_bot.services.locale import Localizator
from seeds_shop.tg_bot.services.tg_helpers import broadcast, send_tg_message

logger = logging.getLogger(__name__)


async def confirm_order_payment(call: types.CallbackQuery, _, manager: DialogManager):
    """Подтверждаем оплату заказа"""

    bot: Bot = manager.middleware_data.get("bot")
    localizator: Localizator = manager.middleware_data.get("localizator")
    locale: TranslatorRunner = manager.middleware_data.get("locale")
    config: Settings = manager.middleware_data.get("config")
    user_service: UserService = manager.middleware_data.get("user_service")
    order_service: OrderService = manager.middleware_data.get("order_service")
    shop_service: ShopService = manager.middleware_data.get("shop_service")
    bonus_service: BonusService = manager.middleware_data.get("bonus_service")
    bot_settings_service: BotSettingsService = manager.middleware_data.get("bot_settings_service")

    order_id: int = manager.dialog_data.get("order_id")
    order = await order_service.get_order_by_id(order_id)
    await shop_service.get_shop_by_id(order.shop_id)
    order_owner = await user_service.get_user_by_id(order.buyer_db_id)
    bot_settings = await bot_settings_service.get_bot_settings()

    await order_service.update_order_status(int(order_id), OrderStatus.payment_confirmed)
    await send_tg_message(
        bot,
        config.tg_bot.admin_channel_id,
        locale.get(
            "order-status-changed-msg",
            order_id=order_id,
            status=OrderStatus.payment_confirmed.value,
        ),
    )
    # Добавляем бонусы пользователю за заказ
    bonuses_for_order = calculate_bonuses_for_order(order.original_summ, bot_settings.maximum_bonus_for_order_percent)
    await bonus_service.create_operation(order_owner.id, OperationType.ACCRUAL, amount=bonuses_for_order)

    # Отправляем уведомление для отгрузки сотрудникам склада в магазине
    stuff = await user_service.get_users_by_role_and_shop_id(UserRole.stuff, order.shop_id)
    await broadcast(
        bot,
        stuff,
        locale.get("new-order-for-shipping-msg", order_id=order_id),
        reply_markup=order_shipping_kb(locale, order_id),
    )

    # Отправляем сообщение о сборке заказа покупателю
    user_locale: TranslatorRunner = localizator.get_by_locale(order_owner.lang_code)

    await send_tg_message(bot, order_owner.telegram_id, user_locale.get("order-collecting-msg"))
    await send_tg_message(
        bot,
        order_owner.telegram_id,
        locale.get(
            "bonuses-credited-for-order",
            bonuses_amount=bonuses_for_order,
            days_before_using_bonuses=bot_settings.days_before_using_bonus,
        ),
    )

    await call.answer(locale.get("order-payment-confirmed-msg"))
    await manager.done()


async def process_tracking_link(message: types.Message, _, manager: DialogManager, tracking_link: str):
    """Обрабатываем ссылку на отслеживание заказа"""

    manager.dialog_data["tracking_link"] = tracking_link

    await manager.next()


async def change_order_tracking_link(call: types.CallbackQuery, _, manager: DialogManager):
    """Обновляем ссылку на отслеживание в заказе"""

    bot: Bot = manager.middleware_data.get("bot")
    locale: TranslatorRunner = manager.middleware_data.get("locale")
    config: Settings = manager.middleware_data.get("config")
    order_service: OrderService = manager.middleware_data.get("order_service")
    user_service: UserService = manager.middleware_data.get("user_service")
    manager.middleware_data.get("bonus_service")
    bot_settings_service: BotSettingsService = manager.middleware_data.get("bot_settings_service")
    payment_method_service: PaymentMethodService = manager.middleware_data.get("payment_method_service")

    order_id: int = manager.dialog_data.get("order_id")
    tracking_link: str = manager.dialog_data.get("tracking_link")

    order = await order_service.get_order_by_id(order_id)
    order_owner = await user_service.get_user_by_id(order.buyer_db_id)
    await payment_method_service.get_payment_method_by_id(order.payment_method_id)
    await bot_settings_service.get_bot_settings()

    await order_service.update_order_tracking_link(order_id, tracking_link)

    await send_tg_message(
        bot,
        config.tg_bot.admin_channel_id,
        locale.get(
            "order-status-changed-msg",
            order_id=order_id,
            status=OrderStatus.in_transit.value,
        ),
    )
    await send_tg_message(
        bot,
        order_owner.telegram_id,
        locale.get("order-in-transit-msg", tracking_link=tracking_link),
        reply_markup=after_order_kb(locale),
    )

    await call.answer(locale.get("order-tracking-link-changed-msg"))

    await manager.done()


async def close_order(_, __, manager: DialogManager):
    """Закрываем заказ"""

    bot: Bot = manager.middleware_data.get("bot")
    config: Settings = manager.middleware_data.get("config")
    locale: TranslatorRunner = manager.middleware_data.get("locale")
    order_service: OrderService = manager.middleware_data.get("order_service")

    order_id: int = manager.dialog_data.get("order_id")
    await order_service.update_order_status(order_id, OrderStatus.closed)

    await send_tg_message(
        bot,
        config.tg_bot.admin_channel_id,
        locale.get(
            "order-status-changed-msg",
            order_id=order_id,
            status=OrderStatus.closed.value,
        ),
    )
