"""
auth feature configuration.

Injects environment variables into Flask app.config.
Add your feature's env vars here so the framework can track them.

To regenerate from source code: splent feature:inject-config splent_feature_auth
"""

import os


def inject_config(app):
    # An unset or empty value shows the entry, because a product that
    # installs auth almost always wants a visible way in, and a blank line
    # in a .env must not quietly remove the only one.
    nav_login = os.getenv("AUTH_NAV_LOGIN", "")

    # The shell the sign-in page renders in. A reader following the link
    # from a public page in Spanish used to land in the admin dashboard,
    # in English, with none of the site they came from around it. That is
    # right for a back office and wrong for a front door, so a product with
    # a public shell names it here.
    #
    # Empty means the admin shell, which is what a product that is only a
    # back office has and what every existing product got before this
    # existed.
    login_layout = os.getenv("AUTH_LOGIN_LAYOUT", "").strip()

    app.config.update(
        {
            # "Log in" (or "Log out") in the public header. A site with no
            # members area, where staff reach the panel by typing the URL,
            # sets this to false.
            "AUTH_NAV_LOGIN": nav_login.strip().lower() not in ("0", "false", "no"),
            "AUTH_LOGIN_LAYOUT": login_layout or None,
        }
    )
