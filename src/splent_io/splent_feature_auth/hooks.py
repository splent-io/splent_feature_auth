from splent_framework.hooks.template_hooks import register_template_hook
from flask import current_app, render_template, url_for


# ── Sidebar hooks ─────────────────────────────────────────────────────────────


def login_signup_items():
    return render_template("hooks/anonymous_sidebar_items.html")


def logout_item():
    return render_template("hooks/authenticated_sidebar_items.html")


register_template_hook("layout.anonymous_sidebar", login_signup_items)
register_template_hook("layout.authenticated_sidebar", logout_item)


# ── Navbar hooks ──────────────────────────────────────────────────────────────


def navbar_anonymous():
    return render_template("hooks/navbar_anonymous.html")


def navbar_authenticated():
    return render_template("hooks/navbar_authenticated.html")


register_template_hook("layout.navbar.anonymous", navbar_anonymous)
register_template_hook("layout.navbar.authenticated", navbar_authenticated)


# ── Public navigation ────────────────────────────────────────────────────────


def public_nav_account():
    """The way in, in the public header.

    The navbar hooks above belong to the admin shell, so a product whose
    front end is the theme's public shell had no visible way to sign in at
    all: you had to know the URL. This is a hook rather than a nav registry
    entry because the entry differs per request, which a static declaration
    cannot express.

    A product with no members area can turn it off with AUTH_NAV_LOGIN=false.
    """
    if not current_app.config.get("AUTH_NAV_LOGIN", True):
        return ""
    return render_template("hooks/public_nav.html")


register_template_hook("layout.nav", public_nav_account)


# ── Script hooks ─────────────────────────────────────────────────────────────


def auth_scripts():
    return (
        '<script src="'
        + url_for("auth.assets", subfolder="dist", filename="auth.bundle.js")
        + '"></script>'
    )


register_template_hook("layout.scripts", auth_scripts)
