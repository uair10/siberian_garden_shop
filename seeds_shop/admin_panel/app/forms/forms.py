from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators, widgets


class OperateForm(FlaskForm):
    pass


class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        # add WYSIWYG class to existing classes
        existing_classes = kwargs.pop("class", "") or kwargs.pop("class_", "")
        kwargs["class"] = "{} {}".format(existing_classes, "ckeditor")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class SearchForm(FlaskForm):
    q = StringField(
        label="Search",
        validators=[validators.DataRequired()],
        render_kw={
            "placeholder": "Search",
            "class": "form-control form-control-sm mr-3 w-75",
        },
    )


class CreateForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[validators.DataRequired(), validators.Length(1, 256)],
        render_kw={"class": "form-control"},
    )
