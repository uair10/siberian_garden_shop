from flask_login import current_user

from seeds_shop.admin_panel.app.views.base import MyBaseModelView


class AdminUserBaseModelview(MyBaseModelView):
    def is_accessible(self):
        try:
            if current_user.can_create_admins:
                return True
        except AttributeError:
            return False

        return False

    column_exclude_list = "password"

    column_details_exclude_list = "password"

    column_export_exclude_list = "password"

    column_list = (
        "email",
        "password",
        "name",
        "can_create_admins",
        "can_edit",
        "can_export",
        "can_delete",
        "can_add",
        "can_view_files",
    )

    column_labels = {
        "email": "Почта",
        "password": "Пароль",
        "name": "Имя",
        "can_create_admins": "Может создавать админов",
        "can_edit": "Может редактировать записи",
        "can_export": "Может экспортировать записи",
        "can_delete": "Может удалять записи",
        "can_add": "Может создавать записи",
        "can_view_files": "Есть доступ к файлам",
    }

    column_searchable_list = column_list

    def on_model_change(self, form, model, is_created):
        model.set_password(form.password.data)
        super().on_model_change(form, model, is_created)
