"""
End-to-end tests for splent_feature_auth.

E2E tests drive a real browser via Selenium against the running
application.  They are slow by design and should only verify
critical user flows that cannot be covered by functional tests.

Run with:  splent feature:test splent_feature_auth --e2e
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from splent_framework.environment.host import get_host_for_selenium_testing
from splent_framework.selenium.common import initialize_driver, close_driver


@pytest.fixture()
def browser():
    driver = initialize_driver()
    yield driver
    close_driver(driver)


def test_login_and_check_element(browser):
    host = get_host_for_selenium_testing()

    browser.get(f"{host}/login")

    email_field = browser.find_element(By.NAME, "email")
    password_field = browser.find_element(By.NAME, "password")

    email_field.send_keys("user1@example.com")
    password_field.send_keys("1234")
    password_field.send_keys(Keys.RETURN)

    assert "login" not in browser.current_url, "Login failed — still on login page"
