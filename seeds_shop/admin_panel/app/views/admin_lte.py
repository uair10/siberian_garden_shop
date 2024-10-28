from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView


class AdminLTEModelView(ModelView):
    list_template = "flask-admin/model/list.html"
    create_template = "flask-admin/model/create.html"
    edit_template = "flask-admin/model/edit.html"
    details_template = "flask-admin/model/details.html"

    create_modal_template = "flask-admin/model/modals/create.html"
    edit_modal_template = "flask-admin/model/modals/edit.html"
    details_modal_template = "flask-admin/model/modals/details.html"


class AdminLTEFileAdmin(FileAdmin):
    list_template = "flask-admin/file/list.html"

    upload_template = "flask-admin/file/form.html"
    mkdir_template = "flask-admin/file/form.html"
    rename_template = "flask-admin/file/form.html"
    edit_template = "flask-admin/file/form.html"

    upload_modal_template = "flask-admin/file/modals/form.html"
    mkdir_modal_template = "flask-admin/file/modals/form.html"
    rename_modal_template = "flask-admin/file/modals/form.html"
    edit_modal_template = "flask-admin/file/modals/form.html"
