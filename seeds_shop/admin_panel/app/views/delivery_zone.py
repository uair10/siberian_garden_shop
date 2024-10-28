from seeds_shop.admin_panel.app.views import MyBaseModelView


class DeliveryZoneModelView(MyBaseModelView):
    column_list = (
        "title",
        "shops",
    )

    form_excluded_columns = ("created_at", "updated_at", "users", "stocks", "orders")

    column_labels = {
        "title": "Название",
        "admin_users": "Админы",
        "shops": "Магазины",
    }
