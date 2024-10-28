from seeds_shop.admin_panel.app.formatters import enum_type_formatter
from seeds_shop.admin_panel.app.views import MyBaseModelView


class TicketModelView(MyBaseModelView):
    column_list = (
        "admin",
        "status",
        "telegram_id",
        "username",
        "order",
        "created_at",
        "updated_at",
    )

    form_excluded_columns = ("created_at", "updated_at")

    column_formatters = {"status": enum_type_formatter}

    column_labels = {
        "admin": "Ответственный",
        "status": "Статус",
        "telegram_id": "ID клиента",
        "username": "Ник клиента",
        "order": "Привязан к заказу",
        "created_at": "Создан",
        "updated_at": "Обновлен",
    }
