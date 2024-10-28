from decimal import ROUND_DOWN, Decimal

from seeds_shop.core.models.dto.discount import DiscountDTO
from seeds_shop.core.models.dto.product import ProductDTO, ProductWithQuantityDTO
from seeds_shop.core.models.enums.currency import Currency
from seeds_shop.core.models.enums.price_calculation import BonusesApplyStrategy, PromocodeApplyStrategy


def convert_currency(
    summ: Decimal, currency_to: Currency, exchange_rate: Decimal, exchange_percent: Decimal | None = None
) -> Decimal:
    """Конвертируем из одной валюты в другую"""

    converted = summ / exchange_rate

    if exchange_percent:
        converted += (converted / Decimal("100")) * Decimal(exchange_percent)

    return (
        converted.quantize(Decimal("0.000001"), rounding=ROUND_DOWN)
        if currency_to == Currency.btc
        else converted.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
    )


def get_max_discount(discounts: list[DiscountDTO], quantity: int, category_id: int) -> DiscountDTO | None:
    return max(
        (
            discount
            for discount in discounts
            if discount.required_quantity <= quantity and discount.category_id == category_id
        ),
        key=lambda discount: discount.discount_percent,
        default=None,
    )


def get_bonuses_for_product(
    product_price: Decimal,
    product_quantity: int,
    total_sum: Decimal,
    maximum_discount_percent: float,
    bonuses_amount: float,
) -> Decimal:
    """
    Получаем количество бонусов на единицу товара
    :param product_price: Цена товара
    :param product_quantity: Кол-во товара
    :param total_sum: Общая сумма всех товаров
    :param maximum_discount_percent: Максимальный процент скидки за бонусы
    :param bonuses_amount: Кол-во бонусов
    """

    max_bonuses = min(Decimal(bonuses_amount), total_sum * (Decimal(maximum_discount_percent) / 100))
    item_percentage = ((product_price * Decimal(product_quantity)) / total_sum).quantize(Decimal("0.01"))
    item_bonuses = max_bonuses * item_percentage.quantize(Decimal("0.01"))

    return item_bonuses / product_quantity


def calculate_product_discounted_price(
    product: ProductDTO,
    product_quantity: int,
    products: list[ProductWithQuantityDTO],
    maximum_bonus_discount_percent: float,
    discounts: list[DiscountDTO],
    currency: Currency = Currency.rub,
    exchange_rate: Decimal | None = None,
    exchange_percent: Decimal | None = None,
    promocode_percent: Decimal | None = None,
    bonuses_amount: float | None = None,
    promocode_apply_strategy: PromocodeApplyStrategy = PromocodeApplyStrategy.TO_DISCOUNTED_PRICE,
    bonuses_apply_strategy: BonusesApplyStrategy = BonusesApplyStrategy.TO_DISCOUNTED_PRICE,
) -> Decimal:
    """
    Расчитываем цену со скидкой на товар
    :param product: Товар
    :param product_quantity: Кол-во товара
    :param products: Остальные товары в корзине
    :param maximum_bonus_discount_percent: Максимальный процент скидки за бонусы
    :param discounts: Список скидок по текущему магазину
    :param currency: Текущая валюта заказа
    :param exchange_rate: Обменный курс
    :param exchange_percent: Добавочный процент при конвертации валюты
    :param promocode_percent: Сумма промокода в %
    :param bonuses_amount: Кол-во бонусов
    :param promocode_apply_strategy: Стратегия добавления промокода (к изначальной цене или к цене со скидкой)
    :param bonuses_apply_strategy: Стратегия добавления бонусов (к изначальной цене или к цене со скидкой)
    """

    product_price = Decimal(str(product.price))

    # Считаем сумму корзины для получения процента товара в ней
    cart_total = sum((p.product.price * p.quantity) for p in products)

    category_products_quantity = sum(p.quantity for p in products if p.product.category_id == product.category_id)
    discount = get_max_discount(discounts, category_products_quantity, product.category_id)
    if not discount or not discount.works_inside_category:
        discount = get_max_discount(discounts, product_quantity, product.category_id)

    discounted_price = (
        product_price - (product_price * Decimal(discount.discount_percent) / 100) if discount else product_price
    )

    if promocode_percent:
        old_price = (
            product_price if promocode_apply_strategy == PromocodeApplyStrategy.TO_ORIGINAL_PRICE else discounted_price
        )  # TODO Протестировать
        discounted_price = old_price - old_price * (Decimal(promocode_percent / 100))

    # Применяем бонусы к корзине
    if bonuses_amount and bonuses_amount > 0:
        old_price = (
            product_price if bonuses_apply_strategy == BonusesApplyStrategy.TO_ORIGINAL_PRICE else discounted_price
        )  # TODO Протестировать
        product_bonuses = get_bonuses_for_product(
            product_price,
            product_quantity,
            Decimal(cart_total),
            maximum_bonus_discount_percent,
            bonuses_amount,
        )
        discounted_price = old_price - product_bonuses

    if currency != Currency.rub and exchange_rate:
        discounted_price = convert_currency(
            summ=discounted_price, currency_to=currency, exchange_rate=exchange_rate, exchange_percent=exchange_percent
        )

    return discounted_price


def calculate_total_summ(
    products: list[ProductWithQuantityDTO],
    maximum_bonus_discount_percent: float,
    discounts: list[DiscountDTO],
    paid_delivery_enabled: bool,
    delivery_price: Decimal,
    free_delivery_threshold: Decimal,
    currency: Currency = Currency.rub,
    exchange_rate: Decimal | None = None,
    exchange_percent: Decimal | None = None,
    promocode_percent: Decimal | None = None,
    bonuses_amount: float | None = None,
) -> Decimal:
    """Расcчитываем сумму заказа / корзины с учетом валюты, скидок и промокода"""

    total_summ = Decimal(0)
    for product in products:
        total_summ += (
            calculate_product_discounted_price(
                product=product.product,
                product_quantity=product.quantity,
                products=products,
                maximum_bonus_discount_percent=maximum_bonus_discount_percent,
                discounts=discounts,
                currency=currency,
                exchange_rate=exchange_rate,
                exchange_percent=exchange_percent,
                promocode_percent=promocode_percent,
                bonuses_amount=bonuses_amount,
            )
            * product.quantity
        )
    delivery_cost = calculate_delivery_cost(
        paid_delivery_enabled=paid_delivery_enabled,
        delivery_price=delivery_price,
        order_summ=total_summ,
        free_delivery_threshold=free_delivery_threshold,
        currency=currency,
        exchange_rate=exchange_rate,
        exchange_percent=exchange_percent,
    )
    return total_summ + delivery_cost


def calculate_bonuses_for_order(order_summ: Decimal, maximum_bonus_for_order_percent: float) -> int:
    """
    Рассчитываем количество бонусов за заказ
    :param order_summ: Сумма заказа
    :param maximum_bonus_for_order_percent: Процент бонусов от цены заказа
    """

    return int((order_summ / 100) * Decimal(maximum_bonus_for_order_percent))


def calculate_delivery_cost(
    paid_delivery_enabled: bool,
    delivery_price: Decimal,
    order_summ: Decimal,
    free_delivery_threshold: Decimal,
    currency: Currency = Currency.rub,
    exchange_rate: Decimal | None = None,
    exchange_percent: Decimal | None = None,
) -> Decimal:
    """Рассчитываем стоимость доставки"""

    if not paid_delivery_enabled:
        return Decimal(0)
    if order_summ > free_delivery_threshold:
        return Decimal(0)

    if currency != Currency.rub and exchange_rate:
        return convert_currency(
            summ=delivery_price, currency_to=currency, exchange_rate=exchange_rate, exchange_percent=exchange_percent
        )

    return delivery_price
