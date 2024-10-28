from seeds_shop.admin_panel.app.views import MyBaseModelView


class ReviewModelView(MyBaseModelView):
    column_list = (
        "review_text",
        "user",
        "created_at",
    )

    form_excluded_columns = ("created_at", "updated_at")

    column_labels = {
        "review_text": "Текст отзыва",
        "user": "Автор",
        "created_at": "Создан",
    }
