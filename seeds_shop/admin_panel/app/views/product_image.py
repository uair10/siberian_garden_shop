import logging

from flask import Markup, url_for
from flask_admin import form

from seeds_shop.admin_panel.app.constants import images_folder
from seeds_shop.admin_panel.app.formatters import generate_product_filename
from seeds_shop.admin_panel.app.views import MyBaseModelView

logger = logging.getLogger(__name__)


class ProductImageModelView(MyBaseModelView):
    @staticmethod
    def _list_thumbnail(cls, context, model, name):
        if not model.image_path:
            return ""

        url = url_for("media_bp.product_images", filename=model.image_path)
        return Markup(f"<img style='max-width: 50px;' src='{url}'>")

    column_list = (
        "image_path",
        "product",
        "created_at",
    )

    column_formatters = {"image_path": _list_thumbnail}

    form_excluded_columns = (
        "created_at",
        "updated_at",
    )

    column_filters = ("product",)

    form_extra_fields = {
        "image_path": form.ImageUploadField(
            "Фото",
            base_path=images_folder,
            namegen=generate_product_filename,
            allow_overwrite=True,
            allowed_extensions=["png", "jpg", "jpeg"],
            endpoint="media_bp.product_images",
        ),
    }

    column_labels = {
        "product": "Товар",
        "image_path": "Фото",
        "created_at": "Создан",
    }
