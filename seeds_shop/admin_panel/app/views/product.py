import logging

from flask import Markup, flash, url_for
from wtforms import StringField

from seeds_shop.admin_panel.app.formatters import _stock_formatter
from seeds_shop.admin_panel.app.views import MyBaseModelView
from seeds_shop.infrastructure.database.models import Product, Shop, Stock

logger = logging.getLogger(__name__)


class ProductModelView(MyBaseModelView):
    @staticmethod
    def _list_thumbnail(cls, context, model: Product, name):
        if not model.images:
            return ""
        images = ""
        for image in model.images:
            url = url_for("media_bp.product_images", filename=image.image_path)
            images += f"<img style='max-width: 50px;' src='{url}'>"
        return Markup(images)

    def on_model_change(self, form, model, is_created):
        if is_created:
            try:
                self.session.add(model)
                self.session.flush()
                for shop in self.session.query(Shop).all():
                    model.stock.append(Stock(product_id=model.id, shop_id=shop.id, available_quantity=1))
                self.session.commit()
                flash("Обновите остатки по этому товару в магазинах", "warning")
            except Exception as e:
                logger.exception(e)
                self.session.rollback()
                flash(
                    "Ошибка при создании остатков в магазинах. Создайте их вручную",
                    "error",
                )

    column_list = (
        "id",
        "title",
        "price",
        "images",
        "category",
        "stock",
        "sold_count",
        "webapp_position",
        "cost_to_business",
        "realise_price",
        "sync_with_loyverse",
        "sync_stock_with_loyverse",
        "sku",
        "created_at",
    )

    column_formatters = {"stock": _stock_formatter, "images": _list_thumbnail}

    form_excluded_columns = (
        "cart_products",
        "images",
        "weight",
        "sold_count",
        "order_lines",
        "created_at",
        "updated_at",
    )

    column_filters = (
        "title",
        "price",
        "stock",
        "sold_count",
        "strain_type",
        "origin",
    )

    column_editable_list = ("webapp_position",)

    column_labels = {
        "title": "Название",
        "description": "Описание",
        "measurement": "Единица измерения",
        "price": "Цена в батах",
        "category": "Категория",
        "stock": "Остатки в магазинах",
        "sold_count": "Продаж",
        "available_quantity": "Доступное количество",
        "images": "Фото",
        "webapp_position": "Позиция в вебаппе",
        "sync_with_loyverse": "Синхронизировать с loyverse",
        "sync_stock_with_loyverse": "Синхронизировать остаток с loyverse",
        "created_at": "Создан",
    }

    form_extra_fields = {"sku": StringField("SKU")}
