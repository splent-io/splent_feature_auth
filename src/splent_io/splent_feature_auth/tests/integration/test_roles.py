"""
Integration tests for the role column and the shared role_required gate.

The contract is least privilege: a user created without an explicit role is
"user", and role_required denies anyone whose role is not in the allowed
set. Products keep their pre-role behaviour through the migration backfill
(existing rows become "admin"), which is exercised at the migration level,
not here.
"""

import pytest
from werkzeug.exceptions import Forbidden

from flask_login import login_user
from splent_framework.db import db
from splent_framework.decorators.decorators import role_required
from splent_io.splent_feature_auth.models import User
from splent_io.splent_feature_auth.services import AuthenticationService


def _make_user(email, role="user", active=True):
    user = User(email=email, active=active, role=role)
    user.set_password("1234")
    db.session.add(user)
    db.session.commit()
    return user


def test_new_user_defaults_to_least_privilege(test_app):
    with test_app.app_context():
        user = _make_user("plain@example.com")
        assert user.role == "user"
        assert user.has_role("user") is True
        assert user.has_role("admin", "staff") is False


def test_create_user_service_defaults_to_user_role(test_app):
    with test_app.app_context():
        user = AuthenticationService().create_user(
            email="svc-default@example.com", password="1234"
        )
        assert user.role == "user"


def test_create_user_service_accepts_explicit_role(test_app):
    with test_app.app_context():
        user = AuthenticationService().create_user(
            email="svc-staff@example.com", password="1234", role="staff"
        )
        assert user.role == "staff"


def test_role_required_allows_matching_role(test_app):
    with test_app.test_request_context():
        user = _make_user("staff@example.com", role="staff")
        login_user(user)

        @role_required("staff", "admin")
        def view():
            return "ok"

        assert view() == "ok"


def test_role_required_denies_other_roles(test_app):
    with test_app.test_request_context():
        user = _make_user("student@example.com", role="user")
        login_user(user)

        @role_required("staff", "admin")
        def view():
            return "ok"

        with pytest.raises(Forbidden):
            view()


def test_role_required_denies_inactive_users(test_app):
    with test_app.test_request_context():
        user = _make_user("dormant@example.com", role="staff", active=False)
        login_user(user)

        @role_required("staff")
        def view():
            return "ok"

        with pytest.raises(Forbidden):
            view()


def test_role_required_sends_anonymous_to_login(test_app):
    with test_app.test_request_context():

        @role_required("staff")
        def view():
            return "ok"

        response = view()
        assert response != "ok"
        assert response.status_code == 302
