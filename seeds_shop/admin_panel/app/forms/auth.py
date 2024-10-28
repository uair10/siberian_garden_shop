from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(message="EMAIL_NOT_PROVIDED")])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField(
        "Login",
        render_kw={"class": "btn btn-primary btn-block", "style": "width: 320px;"},
    )


class EditProfileForm(FlaskForm):
    username = StringField(
        label="User Name",
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-sm"},
    )

    email = StringField(
        label="Email Address",
        validators=[DataRequired(), Length(1, 64)],
        render_kw={"class": "form-control form-control-sm"},
    )

    first_name = StringField(
        label="First Name",
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-sm"},
    )

    last_name = StringField(
        label="Last Name",
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-sm"},
    )

    location = StringField(
        label="Address",
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-sm"},
    )

    website = StringField(
        label="Website",
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-sm"},
    )

    bio = TextAreaField(
        label="About me",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Basic textarea",
            "class": "form-control md-textarea",
        },
    )

    submit = SubmitField("Submit", render_kw={"class": "btn btn-primary btn-block"})


class UploadForm(FlaskForm):
    image = FileField(
        "Upload your file",
        validators=[
            FileRequired(),
            FileAllowed(
                ["jpg", "png", "jpeg"],
                "The file format should be .jpg or .png or jpeg.",
            ),
        ],
    )
    submit = SubmitField("Upload", render_kw={"class": "btn btn-primary btn-md"})


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(
        "Old Password",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    password = PasswordField(
        "New Password",
        validators=[DataRequired(), Length(8, 128), EqualTo("password2")],
        render_kw={"class": "form-control"},
    )
    password2 = PasswordField(
        "Confirm Password",
        validators=[DataRequired()],
        render_kw={"class": "form-control"},
    )
    submit = SubmitField(render_kw={"class": "btn btn-primary btn-md"})
