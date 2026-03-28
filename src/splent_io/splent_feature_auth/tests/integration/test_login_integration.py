def test_login_sets_session_cookie(test_client, auth_test_user):
    response = test_client.post(
        "/login",
        data={"email": "user1@example.com", "password": "1234"},
        follow_redirects=True,
    )

    # After successful login, the user is redirected to the home page (HTTP 200)
    assert response.status_code == 200
    # The "Log out" link is rendered by auth's hook on the authenticated sidebar
    assert b"Log out" in response.data or b"logout" in response.data
