"""
Integration tests for e-mail availability.

Sign-up creates users inactive, so availability cannot be answered with the
active-only lookup that login uses. Getting this wrong reports a
just-registered address as free, and the insert then dies on the unique
index with a 500 instead of a readable message.
"""

from splent_framework.db import db
from splent_io.splent_feature_auth.models import User
from splent_io.splent_feature_auth.services import AuthenticationService


def _make_user(email, active):
    user = User(email=email, active=active)
    user.set_password("1234")
    db.session.add(user)
    db.session.commit()


def test_inactive_address_is_not_available(test_app):
    """The regression: a freshly registered account is inactive."""
    with test_app.app_context():
        _make_user("pending@example.com", active=False)
        assert AuthenticationService().is_email_available("pending@example.com") is False


def test_active_address_is_not_available(test_app):
    with test_app.app_context():
        _make_user("taken@example.com", active=True)
        assert AuthenticationService().is_email_available("taken@example.com") is False


def test_unknown_address_is_available(test_app):
    with test_app.app_context():
        assert AuthenticationService().is_email_available("free@example.com") is True


def test_login_still_ignores_inactive_accounts(test_app):
    """Availability changed, authentication must not: disabled accounts
    still cannot log in."""
    with test_app.app_context():
        _make_user("disabled@example.com", active=False)
        service = AuthenticationService()
        assert service.repository.get_by_email("disabled@example.com") is None
        assert service.repository.email_exists("disabled@example.com") is True
