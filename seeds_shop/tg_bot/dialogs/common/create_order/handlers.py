import logging
import os
from datetime import timedelta

from aiogram import Bot, types
from aiogram_dialog import DialogManager
from arq import ArqRedis
from arq.jobs import Job
from fluentogram import TranslatorRunner

from seeds_shop.core.config import Settings
from seeds_shop.core.constants import INVOICES_FOLDER
from seeds_shop.core.converters.product import convert_products_to_products_with_quantity
from seeds_shop.core.exceptions.bonus import InsufficientBonuses
from seeds_shop.core.exceptions.order import InsufficientStock
from seeds_shop.core.models.enums.order import OrderStatus
from seeds_shop.core.models.enums.user import UserRole
from seeds_shop.core.price_calculation import calculate_delivery_cost, calculate_total_summ
from seeds_shop.core.services import (
    BotSettingsService,
    DiscountService,
    OrderService,
    PaymentMethodService,
    ProductService,
    PromocodeService,
    ShopService,
    StatsService,
    UserService,
)
from seeds_shop.core.services.delivery_method import DeliveryMethodService
from seeds_shop.core.utils.date_time import get_current_timestamp
from seeds_shop.core.utils.files import get_file_extension
from seeds_shop.infrastructure.currency_converter import get_currency_rate
from seeds_shop.infrastructure.database.converters.order import convert_cart_lines_to_order_line
from seeds_shop.infrastructure.database.redis import CartManager
from seeds_shop.infrastructure.formatters.product import format_product_line
from seeds_shop.tg_bot.keyboards.inline import go_to_shopping_kb, order_payment_confirmation_kb
from seeds_shop.tg_bot.services.tg_helpers import answer_msg_with_autodelete, broadcast, delete_msg, send_tg_message

logger = logging.getLogger(__name__)


async def set_city(message: types.Message, _, manager: DialogManager, city_name: str):
    locale: TranslatorRunner = manager.middleware_data.get("locale")
    delivery_method_service: DeliveryMethodService = manager.middleware_data.get("delivery_method_service")
    city = await delivery_method_service.get_city_by_name(city_name)

    if not city or not await delivery_method_service.get_delivery_methods_by_city(city.id):
        await answer_msg_with_autodelete(message, locale.get("city-is-not-supported-yet"))
        return

    manager.dialog_data["city_id"] = city.id
    await manager.next()


async def set_delivery_method(_, __, manager: DialogManager, delivery_method_id: str):
    manager.dialog_data["delivery_method_id"] = int(delivery_method_id)
    await manager.next()


async def set_user_contact_phone(_, __, manager: DialogManager, phone: str):
    manager.dialog_data["buyer_phone"] = phone
    await manager.next()


async def set_user_delivery_address(_, __, manager: DialogManager, address: str):
    manager.dialog_data["delivery_address"] = address
    await manager.next()


async def set_user_postal_code(_, __, manager: DialogManager, postal_code: str):
    address = manager.dialog_data.get("delivery_address")
    manager.dialog_data["delivery_address"] = f"{address} {postal_code}"
    await manager.next()


async def set_user_contact_name(_, __, manager: DialogManager, name: str):
    manager.dialog_data["buyer_name"] = name
    await manager.next()


async def create_or_update_order(call: types.CallbackQuery, __, manager: DialogManager, payment_method_id: str):
    """Создаем заказ из корзины пользователя / обновляем существующий заказ"""

    bot: Bot = manager.middleware_data.get("bot")
    locale: TranslatorRunner = manager.middleware_data.get("locale")
    config: Settings = manager.middleware_data.get("config")
    order_service: OrderService = manager.middleware_data.get("order_service")
    user_service: UserService = manager.middleware_data.get("user_service")
    product_service: ProductService = manager.middleware_data.get("product_service")
    shop_service: ShopService = manager.middleware_data.get("shop_service")
    payment_method_service: PaymentMethodService = manager.middleware_data.get("payment_method_service")
    stats_service: StatsService = manager.middleware_data.get("stats_service")
    discount_service: DiscountService = manager.middleware_data.get("discount_service")
    promocode_service: PromocodeService = manager.middleware_data.get("promocode_service")
    bot_settings_service: BotSettingsService = manager.middleware_data.get("bot_settings_service")
    delivery_method_service: DeliveryMethodService = manager.middleware_data.get("delivery_method_service")
    cart_manager: CartManager = manager.middleware_data.get("cart_manager")

    arq_redis: ArqRedis = manager.middleware_data.get("arqredis")

    manager.dialog_data["payment_method_id"] = int(payment_method_id)

    payment_method = await payment_method_service.get_payment_method_by_id(int(payment_method_id))
    delivery_method = await delivery_method_service.get_delivery_method_by_id(
        manager.dialog_data.get("delivery_method_id")
    )
    bot_settings = await bot_settings_service.get_bot_settings()
    user = await user_service.get_user_by_telegram_id(call.from_user.id)
    shop = await shop_service.get_shop_by_delivery_zone_id(user.delivery_zone_id)
    discounts = await discount_service.get_discounts_for_shop(shop.id)

    promocode_value = 0
    if promocode_id := manager.dialog_data.get("promocode_id"):
        promocode = await promocode_service.get_promocode_by_id(promocode_id)
        promocode_value = promocode.amount

    bonuses_amount: int = manager.dialog_data.get("bonuses_amount")
    order_id: int = manager.start_data.get("order_id") or manager.dialog_data.get("order_id")

    exchange_rate = await get_currency_rate(payment_method.currency)
    if not exchange_rate:
        raise ValueError(f"Не удалось получить курс валюты {payment_method.currency}")

    if order_id:
        order = await order_service.get_order_by_id(order_id)
        product_lines = order.order_lines
    else:
        cart = await cart_manager.get_cart(call.from_user.id)
        product_lines = cart.lines

    products = [await product_service.get_product_by_id(line.product_id) for line in product_lines]
    products_with_quantity = convert_products_to_products_with_quantity(product_lines, products)
    # Считаем сумму заказа без конвертации
    original_order_summ = calculate_total_summ(
        products=products_with_quantity,
        maximum_bonus_discount_percent=bot_settings.maximum_bonus_discount_percent,
        discounts=discounts,
        promocode_percent=promocode_value,
        bonuses_amount=bonuses_amount,
        paid_delivery_enabled=bot_settings.paid_delivery_enabled,
        delivery_price=delivery_method.price,
        free_delivery_threshold=bot_settings.free_delivery_threshold,
    )
    converted_order_summ = calculate_total_summ(
        products=products_with_quantity,
        maximum_bonus_discount_percent=bot_settings.maximum_bonus_discount_percent,
        discounts=discounts,
        currency=payment_method.currency,
        exchange_rate=exchange_rate,
        exchange_percent=payment_method.exchange_percent,
        promocode_percent=promocode_value,
        bonuses_amount=bonuses_amount,
        paid_delivery_enabled=bot_settings.paid_delivery_enabled,
        delivery_price=delivery_method.price,
        free_delivery_threshold=bot_settings.free_delivery_threshold,
    )
    delivery_cost = calculate_delivery_cost(
        paid_delivery_enabled=bot_settings.paid_delivery_enabled,
        delivery_price=delivery_method.price,
        order_summ=converted_order_summ,
        free_delivery_threshold=bot_settings.free_delivery_threshold,
        currency=payment_method.currency,
        exchange_rate=exchange_rate,
        exchange_percent=payment_method.exchange_percent,
    )

    if order_id:
        # Обновляем сумму и валюту заказа, если он уже создан
        await order_service.update_order_summ(order_id, converted_order_summ)
        await order_service.update_order_payment_method(order_id, payment_method.id)
    else:
        order_lines = convert_cart_lines_to_order_line(product_lines)

        try:
            order = await order_service.create_order(
                summ=converted_order_summ,
                original_summ=original_order_summ,
                user_id=user.id,
                shop_id=shop.id,
                buyer_phone=manager.dialog_data.get("buyer_phone"),
                buyer_name=manager.dialog_data.get("buyer_name"),
                delivery_address=manager.dialog_data.get("delivery_address"),
                delivery_zone_id=user.delivery_zone_id,
                payment_method_id=payment_method.id,
                delivery_method_id=int(manager.dialog_data.get("delivery_method_id")),
                order_lines=order_lines,
                promocode_id=promocode_id,
                bonuses_amount=bonuses_amount,
            )
        except InsufficientStock:
            await call.message.answer(
                locale.get("insufficient-stock-msg"),
                reply_markup=go_to_shopping_kb(locale),
            )
            return
        except InsufficientBonuses:
            await call.message.answer(
                locale.get("insufficient-bonuses"),
                reply_markup=go_to_shopping_kb(locale),
            )
            return

        order_id = order.id
        await stats_service.add_stats(products_purchased=len(order_lines))
        await stats_service.add_stats(orders_created=1)

        await send_tg_message(
            bot,
            config.tg_bot.admin_channel_id,
            locale.get(
                "new-order-msg",
                order_id=order_id,
                shop_id=shop.id,
                order_summ=order.summ,
                currency_symbol=payment_method.currency_symbol.value,
            ),
        )
    order = await order_service.get_order_by_id(order_id)
    # Формируем отображение цен товаров в заказе
    order_product_lines_text = ""
    for line in order.order_lines:
        product = await product_service.get_product_by_id(line.product_id)
        order_product_lines_text += format_product_line(
            product.title,
            line.quantity * line.final_unit_price,
            product.measurement,
            line.quantity,
        )
        await product_service.increase_product_sold_count(line.product_id, line.quantity)

    # Записываем новую сумму заказа в dialog_data
    manager.dialog_data["order_id"] = order_id
    manager.dialog_data["order_summ"] = str(order.summ)
    manager.dialog_data["order_product_lines_text"] = order_product_lines_text
    manager.dialog_data["delivery_cost"] = str(delivery_cost)

    notify_expiring_payment_job = await arq_redis.enqueue_job(
        "notify_expiring_payment",
        user_tg_id=call.from_user.id,
        order_id=order_id,
        _defer_by=timedelta(minutes=50),
    )
    notify_expired_payment_job = await arq_redis.enqueue_job(
        "notify_expired_payment",
        user_tg_id=call.from_user.id,
        order_id=order_id,
        _defer_by=timedelta(hours=1),
    )
    manager.dialog_data["notify_expiring_payment_job_id"] = notify_expiring_payment_job.job_id
    manager.dialog_data["notify_expired_payment_job_id"] = notify_expired_payment_job.job_id

    await manager.next()


async def go_back_with_job_cancel(_, __, manager: DialogManager):
    """
    Переходим назад к выбору способа оплаты
    Отменяем текущие задачи на уведомление пользователя
    """

    arq_redis: ArqRedis = manager.middleware_data.get("arqredis")

    await Job(manager.dialog_data["notify_expiring_payment_job_id"], redis=arq_redis).abort()
    await Job(manager.dialog_data["notify_expired_payment_job_id"], redis=arq_redis).abort()

    await manager.back()


async def process_invoice_screenshot(message: types.Message, _, manager: DialogManager):
    """Валидируем и сохраняем скриншот об оплате заказа"""

    bot: Bot = manager.middleware_data.get("bot")
    locale: TranslatorRunner = manager.middleware_data.get("locale")
    config: Settings = manager.middleware_data.get("config")
    order_service: OrderService = manager.middleware_data.get("order_service")
    user_service: UserService = manager.middleware_data.get("user_service")

    order_id: int = manager.dialog_data.get("order_id")

    if not message.document and not message.photo:
        await answer_msg_with_autodelete(message, locale.get("wrong-input-msg"))
        return

    if message.document:
        file = message.document
        extension = get_file_extension(file.file_name)
        if extension not in ["jpeg", "jpg", "png"]:
            await answer_msg_with_autodelete(message, locale.get("wrong-photo-extension"))
            return

    elif message.photo:
        file = message.photo[-1]

    file = await bot.get_file(file.file_id)
    msg = await message.answer(locale.get("photo-processing-msg"))

    filename = f"{message.from_user.id}_{get_current_timestamp()}.png"

    destination_path = os.path.join(INVOICES_FOLDER, filename)
    await bot.download_file(file.file_path, destination_path)

    await order_service.update_order_invoice_path(order_id, filename)
    await delete_msg(msg)

    await message.answer(locale.get("after-payment-msg"))

    order = await order_service.get_order_by_id(order_id)

    # Отправляем сообщение для подтверждения оплаты админам магазина
    admins = await user_service.get_users_by_role_and_shop_id(UserRole.admin, order.shop_id)
    await broadcast(
        bot,
        admins,
        locale.get("new-order-for-payment-confirmation-msg", order_id=order_id),
        reply_markup=order_payment_confirmation_kb(locale, order_id=order_id),
    )

    await send_tg_message(
        bot,
        config.tg_bot.admin_channel_id,
        locale.get(
            "order-status-changed-msg",
            order_id=order_id,
            status=OrderStatus.payment_not_confirmed.value,
        ),
    )

    await manager.reset_stack()
