from seeds_shop.admin_panel.app.views import MyBaseModelView


class PromocodeModelView(MyBaseModelView):
    column_list = (
        "name",
        "amount",
        "status",
        "limit",
        "reusable",
        "uses_number",
    )

    column_labels = {
        "name": "Имя промокода",
        "amount": "Процент скидки",
        "status": "Статус",
        "limit": "Лимит использований (0 - безлимитный)",
        "reusable": "Можно использовать повторно",
        "users": "Пользователи",
        "orders": "Заказы",
        "uses_number": "Использован раз",
    }

    form_excluded_columns = (
        "shop",
        "orders",
        "users",
        "created_at",
        "updated_at",
    )

    column_editable_list = (
        "limit",
        "reusable",
    )

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
