"""
Functional tests for the auth login flow.

Tests use Flask's test client to exercise full HTTP
request/response cycles (GET, POST, redirects, rendered HTML).
"""

from flask import url_for


def test_login_success(test_client, auth_test_user):
    response = test_client.post(
        "/login",
        data={"email": "user1@example.com", "password": "1234"},
        follow_redirects=True,
    )
    assert b"Invalid credentials" not in response.data


def test_login_unsuccessful_bad_email(test_client):
    response = test_client.post(
        "/login",
        data={"email": "bademail@example.com", "password": "test1234"},
        follow_redirects=True,
    )
    assert response.request.path == url_for("auth.login")


def test_login_unsuccessful_bad_password(test_client, auth_test_user):
    response = test_client.post(
        "/login",
        data={"email": "user1@example.com", "password": "wrongpass"},
        follow_redirects=True,
    )
    assert b"Invalid credentials" in response.data
