from seeds_shop.admin_panel.app.formatters import _orders_formatter
from seeds_shop.admin_panel.app.views import MyBaseModelView


class UserModelView(MyBaseModelView):
    column_list = (
        "id",
        "telegram_id",
        "role",
        "username",
        "created_at",
    )

    form_columns = (
        "telegram_id",
        "role",
        "username",
        "delivery_zone",
        "working_delivery_zone",
        "shop",
        "created_at",
    )

    form_excluded_columns = ("cart", "tickets", "lang_code", "updated_at")

    column_searchable_list = ("telegram_id", "username")

    column_filters = ("telegram_id", "username", "created_at")

    column_labels = {
        "status": "Статус",
        "role": "Роль",
        "shop": "Сотрудник в магазине",
        "telegram_id": "ID в телеграме",
        "username": "Юзернейм в телеграме",
        "lang_code": "Язык",
        "was_created": "Дата создания",
        "orders": "Заказы",
        "delivery_zone": "Зона доставки",
        "working_delivery_zone": "Рабочая зона доставки",
        "reviews": "Отзывы",
        "created_at": "Дата регистрации",
    }

    column_formatters = {"orders": _orders_formatter}

    column_default_sort = ("id", True)
