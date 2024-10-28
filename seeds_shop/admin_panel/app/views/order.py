from flask_admin.form import ImageUploadField

from seeds_shop.admin_panel.app.constants import media_path
from seeds_shop.admin_panel.app.formatters import _order_lines_formatter, _user_formatter, enum_type_formatter
from seeds_shop.admin_panel.app.views import MyBaseModelView


class OrderModelView(MyBaseModelView):
    column_list = (
        "id",
        "status",
        "summ",
        "order_lines",
        "user",
        "delivery_method",
        "shipping_address",
        "buyer_name",
        "payment_method",
        "created_at",
    )

    column_filters = (
        "status",
        "summ",
        "user",
        "delivery_method",
        "payment_method",
    )

    column_formatters = {
        "user": _user_formatter,
        "order_lines": _order_lines_formatter,
        "status": enum_type_formatter,
        "delivery_method": enum_type_formatter,
    }

    form_extra_fields = {
        "invoice_screenshot_path": ImageUploadField(
            "Скриншот оплаты",
            base_path=media_path,
            allow_overwrite=True,
            allowed_extensions=["png", "jpg"],
            endpoint="media_bp.invoices",
        ),
    }

    column_labels = {
        "status": "Статус",
        "summ": "Сумма",
        "order_lines": "Товары в заказе",
        "payment_method": "Метод оплаты",
        "delivery_method": "Метод доставки",
        "user": "Покупатель",
        "shop": "Магазин",
        "tracking_link": "Ссылка для отслеживания",
        "comment": "Комментарий",
        "promocode": "Промокод",
        "shipping_address": "Адрес доставки",
        "buyer_phone": "Номер телефона",
        "buyer_name": "Имя клиента",
        "invoice_screenshot_path": "Скриншот оплаты",
        "bonuses_amount": "Кол-во бонусов",
        "created_at": "Дата создания",
    }

    form_excluded_columns = ("tickets", "updated_at")

    column_default_sort = ("id", True)
