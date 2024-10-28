from seeds_shop.admin_panel.app.formatters import _orders_formatter, _stock_formatter
from seeds_shop.admin_panel.app.views.base import MyBaseModelView


class ShopModelView(MyBaseModelView):
    column_list = ("id", "title", "stock", "delivery_zones")

    column_formatters = {"stock": _stock_formatter, "orders": _orders_formatter}

    form_excluded_columns = ("discounts", "created_at", "updated_at")

    column_labels = {
        "title": "Название",
        "stock": "Остатки товаров",
        "orders": "Заказы",
        "workers": "Работники",
        "delivery_zones": "Зоны доставки",
    }
