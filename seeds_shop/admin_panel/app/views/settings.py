from seeds_shop.admin_panel.app.views import MyBaseModelView


class SettingsModelView(MyBaseModelView):
    column_list = (
        "is_bot_enabled",
        "days_before_using_bonus",
        "maximum_bonus_for_order_percent",
        "maximum_bonus_discount_percent",
        "bot_disabled_until",
    )

    form_excluded_columns = ("created_at", "updated_at")

    column_labels = {
        "is_bot_enabled": "Бот включен",
        "days_before_using_bonus": "Дней перед использованием бонусов",
        "maximum_bonus_for_order_percent": "Процент бонусов за заказ",
        "maximum_bonus_discount_percent": "Макс. процент оплаты заказа бонусами",
        "bot_disabled_until": "Бот отключен до",
    }
