from flask_login import current_user

from seeds_shop.admin_panel.app.views.admin_lte import AdminLTEFileAdmin
from seeds_shop.admin_panel.app.views.auth_mixin import AuthMixin


class MyFileAdmin(AuthMixin, AdminLTEFileAdmin):
    def is_accessible(self):
        try:
            if current_user.can_view_files:
                return True
        except AttributeError:
            return False
        return False

    editable_extensions = ("md", "txt", "html", "css", "log")
