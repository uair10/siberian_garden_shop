from seeds_shop.admin_panel.app.views import MyBaseModelView


class OrderLineModelView(MyBaseModelView):
    column_list = (
        "id",
        "order",
        "product",
        "quantity",
        "created_at",
    )

    column_labels = {
        "status": "Статус",
        "order": "Заказ",
        "product": "Товар",
        "quantity": "Количество",
        "created_at": "Дата создания",
    }

    form_excluded_columns = ("created_at", "updated_at")
