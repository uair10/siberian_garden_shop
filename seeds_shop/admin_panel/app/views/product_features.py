from seeds_shop.admin_panel.app.views import MyBaseModelView


class ProductFeaturesModelView(MyBaseModelView):
    column_list = ("title",)

    form_excluded_columns = ("products", "created_at", "updated_at")

    column_labels = {
        "title": "Название",
    }
