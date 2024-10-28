import os

from flask import Markup
from slugify import slugify
from werkzeug.utils import secure_filename

from seeds_shop.core.utils.date_time import get_current_timestamp
from seeds_shop.infrastructure.database.models import Shop


def enum_type_formatter(view, context, model, name) -> str | None:
    db_value = getattr(model, name)
    if db_value:
        return db_value.value

    return None


def generate_product_filename(obj, file_data, **kwargs):
    """Генерируем название для фото товара"""

    filename, extension = os.path.splitext(file_data.filename)
    filename = filename.replace(filename, slugify(obj.product.title))
    return secure_filename(f"{filename}_{get_current_timestamp()}{extension}")


def generate_payment_filename(obj, file_data, **kwargs):
    """Генерируем название для фото qr кода для оплаты"""

    return secure_filename(f"{obj.currency_symbol}_{get_current_timestamp()}_qr_code.jpg")


def generate_view_url(view_name: str, model_id: int, title: str):
    """
    Генерируем ссылку на связанные модели
    :param view_name: Название роута связанной модели в админке
    :param model_id: Id связанной модели
    :param title: Текст ссылки
    """

    url = f"/{view_name}/details/?id={model_id}"
    return f"<a class='btn btn-default btn-sm' style='margin-left: 0.2rem' title='{title}' href='{url}'>{title}</a>"


def _stock_formatter(view, context, model, name):
    markup = ""
    if model.stock:
        markup += "<div class='btn-group'>"
        for stock in model.stock:
            if isinstance(model, Shop):
                view_name = stock.product_id
            else:
                view_name = stock.shop
            markup += generate_view_url(f"stocks-{stock.shop_id}", stock.id, view_name)
        markup += "</div>"
        return Markup(markup)
    return markup


def _user_formatter(view, context, model, name):
    markup = ""
    if model.user:
        markup += "<div class='btn-group'>"
        markup += generate_view_url("users", model.user.id, model.user.telegram_id)
        markup += "</div>"
        return Markup(markup)
    return markup


def _orders_formatter(view, context, model, name):
    markup = ""
    if model.orders:
        markup += "<div class='btn-group'>"
        for order in model.orders:
            markup += generate_view_url("orders", order.id, order.id)
        markup += "</div>"
        return Markup(markup)
    return markup


def _order_lines_formatter(view, context, model, name):
    markup = ""
    if model.order_lines:
        markup += "<div class='btn-group'>"
        for line in model.order_lines:
            markup += generate_view_url("orders-lines", line.id, line.product_id)
        markup += "</div>"
        return Markup(markup)
    return markup
