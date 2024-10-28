from seeds_shop.admin_panel.app.views import MyBaseModelView


class DeliveryCityModelView(MyBaseModelView):
    column_list = (
        "title",
        "delivery_methods",
    )

    form_excluded_columns = ("created_at", "updated_at")

    column_labels = {"title": "Название", "delivery_methods": "Методы доставки"}
