from flask import render_template, redirect, url_for, request
from flask_babel import gettext as _
from flask_login import current_user, logout_user

from splent_io.splent_feature_auth import auth_bp
from splent_io.splent_feature_auth.decorators import guest_required
from splent_io.splent_feature_auth.forms import LoginForm
from splent_io.splent_feature_auth.services import AuthenticationService


authentication_service = AuthenticationService()


@auth_bp.route("/login", methods=["GET", "POST"])
@guest_required
def login():
    if current_user.is_authenticated:
        return redirect(url_for("public.index"))

    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        if authentication_service.login(form.email.data, form.password.data):
            return redirect(url_for("public.index"))

        return render_template(
            "auth/login_form.html", form=form, error=_("Invalid credentials")
        )

    return render_template("auth/login_form.html", form=form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("public.index"))
