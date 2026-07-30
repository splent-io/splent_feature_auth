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

    app.config.update(
        {
            # "Log in" (or "Log out") in the public header. A site with no
            # members area, where staff reach the panel by typing the URL,
            # sets this to false.
            "AUTH_NAV_LOGIN": nav_login.strip().lower() not in ("0", "false", "no"),
        }
    )
