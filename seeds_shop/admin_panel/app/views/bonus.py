from seeds_shop.admin_panel.app.views import MyBaseModelView


class BonusModelView(MyBaseModelView):
    column_list = ("id", "operation_type", "user", "amount", "created_at")

    form_excluded_columns = "updated_at"

    column_labels = {
        "user": "Пользователь",
        "operation_type": "Тип операции",
        "amount": "Количество баллов",
        "created_at": "Дата создания",
    }

    column_filters = (
        "user",
        "amount",
        "operation_type",
    )
