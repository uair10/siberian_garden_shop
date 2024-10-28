from seeds_shop.admin_panel.app.views import MyBaseModelView


class DeliveryMethodModelView(MyBaseModelView):
    column_list = (
        "title",
        "city",
        "price",
        "duration_days",
    )

    form_excluded_columns = ("created_at", "updated_at")

    column_labels = {
        "title": "Название",
        "city": "Город",
        "price": "Цена",
        "duration_days": "Время доставки в днях",
        "accompanying_message": "Сопроводительное сообщение",
    }
