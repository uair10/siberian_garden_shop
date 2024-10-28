from seeds_shop.admin_panel.app.views import MyBaseModelView


class PromocodesModelView(MyBaseModelView):
    column_labels = {
        "name": "Имя промокода",
        "amount": "Сумма промокода",
        "status": "Статус",
        "limit": "Лимит использований (0 - безлимитный)",
        "reusable": "Можно использовать повторно",
        "type": "Тип",
        "users": "Пользователи",
        "orders": "Заказы",
        "bills": "Счета",
        "uses_number": "Использован раз",
        "created_at": "Дата создания",
    }

    column_filters = (
        "amount",
        "status",
        "limit",
        "reusable",
        "uses_number",
        "created_at",
    )

    column_searchable_list = ("name", "amount")

    column_default_sort = ("id", True)
