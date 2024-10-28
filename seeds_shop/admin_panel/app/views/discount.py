from seeds_shop.admin_panel.app.views import MyBaseModelView


class DiscountModelView(MyBaseModelView):
    column_list = (
        "category",
        "shop",
        "discount_percent",
        "required_quantity",
        "works_inside_category",
    )

    form_excluded_columns = ("created_at", "updated_at")

    column_labels = {
        "category": "Категория",
        "shop": "Магазин",
        "discount_percent": "Процент скидки",
        "required_quantity": "Кол-во товаров",
        "works_inside_category": "Действует внутри категории",
    }
