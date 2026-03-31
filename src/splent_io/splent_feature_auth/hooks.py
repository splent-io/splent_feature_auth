from splent_framework.hooks.template_hooks import register_template_hook
from flask import render_template, url_for


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


# ── Script hooks ─────────────────────────────────────────────────────────────


def auth_scripts():
    return (
        '<script src="'
        + url_for("auth.assets", subfolder="dist", filename="auth.bundle.js")
        + '"></script>'
    )


register_template_hook("layout.scripts", auth_scripts)
