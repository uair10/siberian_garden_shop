from flask import redirect, request, url_for
from flask_login import current_user


class AuthMixin:
    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        return False

    def _handle_view(self, _, **kwargs):
        if not self.is_accessible():
            if not current_user.is_authenticated:
                return redirect("/admin/login")
            return redirect(url_for("admin.index"))

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth_bp.login", next=request.url))
