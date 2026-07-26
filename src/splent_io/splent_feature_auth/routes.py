from flask import current_app, render_template, redirect, url_for, request
from flask_babel import gettext as _
from flask_login import current_user, logout_user
from werkzeug.routing import BuildError

from splent_io.splent_feature_auth import auth_bp
from splent_io.splent_feature_auth.decorators import guest_required
from splent_io.splent_feature_auth.forms import LoginForm
from splent_io.splent_feature_auth.services import AuthenticationService


authentication_service = AuthenticationService()


def landing_url():
    """Where to send a user after logging in or out.

    A product may not install the `public` feature (a storefront that owns
    "/" collides with it), so resolving its endpoint unconditionally raises
    BuildError and turns login into a 500. Products can name their own
    landing endpoint via AUTH_LANDING_ENDPOINT; otherwise `public.index` is
    tried first for backwards compatibility, then the site root.
    """
    endpoint = current_app.config.get("AUTH_LANDING_ENDPOINT", "public.index")
    try:
        return url_for(endpoint)
    except BuildError:
        return "/"


@auth_bp.route("/login", methods=["GET", "POST"])
@guest_required
def login():
    if current_user.is_authenticated:
        return redirect(landing_url())

    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        if authentication_service.login(form.email.data, form.password.data):
            return redirect(landing_url())

        return render_template(
            "auth/login_form.html", form=form, error=_("Invalid credentials")
        )

    return render_template("auth/login_form.html", form=form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(landing_url())
