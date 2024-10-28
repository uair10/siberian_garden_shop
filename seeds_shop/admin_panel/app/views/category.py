from seeds_shop.admin_panel.app.views import MyBaseModelView


class CategoryModelView(MyBaseModelView):
    column_list = ("title", "position_number")

    form_excluded_columns = ("discounts", "created_at", "updated_at")

    column_details_exclude_list = ("created_at", "updated_at")

    column_labels = {
        "title": "Название",
        "products": "Товары",
        "position_number": "Позиция категории в вебаппе",
    }
