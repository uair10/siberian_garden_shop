from flask import flash
from sqlalchemy import and_

from seeds_shop.admin_panel.app.views import MyBaseModelView
from seeds_shop.infrastructure.database.models import Stock


class StockModelView(MyBaseModelView):
    def __init__(self, shop_id: int, model, session, **kwargs):
        super().__init__(model, session, **kwargs)
        self.shop_id = shop_id

    column_list = (
        "product",
        "delivery_zone",
        "available_quantity",
    )

    def on_model_change(self, form, model, is_created):
        if is_created:
            with self.session.no_autoflush:
                if (
                    self.session.query(Stock)
                    .filter(
                        and_(
                            Stock.shop_id == self.shop_id,
                            Stock.product == model.product,
                            Stock.delivery_zone == model.delivery_zone,
                        ),
                    )
                    .first()
                ):
                    flash("Запись для этого продукта уже есть в этом магазине", "error")
                    raise ValueError
            model.shop_id = self.shop_id

    def get_query(self):
        return self.session.query(
            Stock,
        ).filter(Stock.shop_id == self.shop_id)

    form_excluded_columns = ("shop", "created_at")

    column_details_exclude_list = ("created_at",)

    column_editable_list = ("available_quantity",)

    column_filters = ("delivery_zone",)

    column_labels = {
        "shop": "Магазин",
        "product": "Товар",
        "delivery_zone": "Зона доставки",
        "available_quantity": "Доступно к заказу",
        "updated_at": "Последнее обновление",
    }
