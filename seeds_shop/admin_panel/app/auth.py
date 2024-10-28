from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from seeds_shop.admin_panel.app import db, login_manager
from seeds_shop.admin_panel.app.forms.auth import LoginForm
from seeds_shop.infrastructure.database.models import AdminUser

auth_bp = Blueprint("auth_bp", __name__, template_folder="templates", static_folder="static")


@auth_bp.route("/admin/login", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Log-in page for registered users.
    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """

    if current_user.is_authenticated:
        return redirect("/")

    login_user_form = LoginForm()
    if login_user_form.validate_on_submit():
        email = login_user_form.email.data
        password = login_user_form.password.data

        user = db.session.query(AdminUser).filter_by(email=email).first()
        redirect_url = "/"

        if (not user) or (not check_password_hash(user.password, password)):
            flash("Please check your login details and try again.")
            return redirect(request.url)

        login_user(user)
        next_page = request.args.get("next")
        if next_page:
            return redirect(next_page)
        else:
            return redirect(redirect_url)

    return render_template(
        "login.html",
        login_user_form=login_user_form,
    )


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        existing_user = db.session.query(AdminUser).filter_by(email=request.form.get("email")).first()
        if existing_user is None:
            user = AdminUser(email=request.form.get("email"))
            user.set_password(request.form.get("password"))
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect("/")
        flash("This email is already used")
    if current_user.is_authenticated:
        return redirect(url_for("dashboard_bp.home"))

    return render_template(
        "signup.html",
    )


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""

    if user_id is not None:
        try:
            user = db.session.query(AdminUser).get(user_id)
        except:
            user = None
        return user
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("Log in to view this page")
    return redirect(url_for("auth_bp.login"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))
