"""
Unit tests for the post-authentication landing URL.

The auth feature must not assume any particular landing feature is installed.
A storefront product owns "/" itself and therefore cannot install `public`,
so resolving `public.index` there raises BuildError and used to turn both
login and logout into a 500.

These build throwaway Flask apps on purpose: landing_url only reads
current_app.config and the URL map, and mutating the shared product fixture
would leak endpoints into other tests.
"""

import pytest
from flask import Flask

from splent_io.splent_feature_auth.routes import landing_url


def _app(**config):
    app = Flask(__name__)
    app.config.update(config)
    return app


def test_falls_back_to_site_root_when_public_is_absent():
    """The regression: no `public` feature must not mean a crash."""
    with _app().test_request_context():
        assert landing_url() == "/"


def test_uses_public_index_when_the_feature_is_installed():
    """Backwards compatibility for every product that already ships `public`."""
    app = _app()
    app.add_url_rule("/", endpoint="public.index", view_func=lambda: "")
    with app.test_request_context():
        assert landing_url() == "/"


def test_public_index_is_honoured_even_when_it_is_not_the_root():
    app = _app()
    app.add_url_rule("/home", endpoint="public.index", view_func=lambda: "")
    with app.test_request_context():
        assert landing_url() == "/home"


def test_product_can_name_its_own_landing_endpoint():
    app = _app(AUTH_LANDING_ENDPOINT="marketplace.index")
    app.add_url_rule("/marketplace", endpoint="marketplace.index", view_func=lambda: "")
    app.add_url_rule("/home", endpoint="public.index", view_func=lambda: "")
    with app.test_request_context():
        assert landing_url() == "/marketplace"


@pytest.mark.parametrize("endpoint", ["nope.nowhere", "public.index"])
def test_unresolvable_endpoint_degrades_to_the_root(endpoint):
    """A typo in product config, or a missing feature, never raises."""
    app = _app(AUTH_LANDING_ENDPOINT=endpoint)
    with app.test_request_context():
        assert landing_url() == "/"
