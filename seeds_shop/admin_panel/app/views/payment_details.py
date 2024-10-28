from flask_admin import form

from seeds_shop.admin_panel.app.constants import assets_folder
from seeds_shop.admin_panel.app.formatters import generate_payment_filename
from seeds_shop.admin_panel.app.views import MyBaseModelView


class PaymentDetailsModelView(MyBaseModelView):
    column_list = (
        "currency",
        "currency_symbol",
        "payment_address",
        "exchange_rate",
        "exchange_percent",
        "available_for_self_pickup",
        "updated_at",
    )

    form_excluded_columns = ("orders", "created_at", "updated_at")

    column_editable_list = ("exchange_rate", "exchange_percent")

    form_extra_fields = {
        "payment_image_path": form.ImageUploadField(
            "QR код для оплаты",
            base_path=assets_folder,
            namegen=generate_payment_filename,
            allow_overwrite=True,
            allowed_extensions=["png", "jpg", "jpeg"],
            endpoint="media_bp.assets",
        ),
    }

    column_labels = {
        "currency": "Валюта",
        "currency_symbol": "Символ валюты",
        "payment_address": "Карта для оплаты",
        "exchange_rate": "Обменный курс",
        "exchange_percent": "Добавочный %",
        "available_for_self_pickup": "Доступен для самовывоза",
        "updated_at": "Последнее обновление",
    }
