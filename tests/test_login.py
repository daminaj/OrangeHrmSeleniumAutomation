"""
OrangeHRM Login Tests - Core test scenarios.
Tests cover various login cases with Allure reporting.
"""

import pytest
import allure
from test_data.test_data import VALID_CREDENTIALS
from pages.login_page import LoginPage


class TestOrangeHRMLogin:
    """Test suite for OrangeHRM login functionality."""

    @pytest.mark.smoke
    @pytest.mark.login
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login(self, login_page: LoginPage):
        """
        Test successful login with valid credentials.

        Steps:
        1. Navigate to login page
        2. Enter valid username and password
        3. Click login button
        4. Verify Dashboard is displayed

        Expected: User is redirected to Dashboard
        """
        login_page.login(
            VALID_CREDENTIALS["username"],
            VALID_CREDENTIALS["password"]
        )
        assert login_page.is_login_successful(), "Dashboard should be displayed after login"
        assert "dashboard" in login_page.get_current_url().lower()

    @pytest.mark.login
    @allure.severity(allure.severity_level.BLOCKER)
    def test_invalid_username(self, login_page: LoginPage):
        """
        Test login with invalid username.

        Steps:
        1. Enter invalid username
        2. Enter valid password
        3. Click login
        4. Verify error message is displayed

        Expected: Error message "Invalid credentials"
        """
        login_page.login("wronguser", VALID_CREDENTIALS["password"])
        error_msg = login_page.get_error_message()
        assert error_msg, "Error message should be displayed"
        assert "Invalid" in error_msg or "Invalid credentials" in error_msg

    @pytest.mark.login
    @allure.severity(allure.severity_level.BLOCKER)
    def test_invalid_password(self, login_page: LoginPage):
        """
        Test login with invalid password.

        Steps:
        1. Enter valid username
        2. Enter invalid password
        3. Click login
        4. Verify error message is displayed

        Expected: Error message "Invalid credentials"
        """
        login_page.login(VALID_CREDENTIALS["username"], "wrongpass")
        error_msg = login_page.get_error_message()
        assert error_msg, "Error message should be displayed"
        assert "invalid" in error_msg.lower()

    @pytest.mark.login
    @allure.severity(allure.severity_level.CRITICAL)
    def test_empty_username(self, login_page: LoginPage):
        """
        Test login with empty username.

        Steps:
        1. Leave username empty
        2. Enter valid password
        3. Click login
        4. Verify validation error

        Expected: Required field validation message
        """
        login_page.login("", VALID_CREDENTIALS["password"])
        error_msg = login_page.get_error_message()
        assert error_msg, "Error message should be displayed"
        assert "Required" in error_msg or "username" in error_msg.lower() or "empty" in error_msg.lower()

    @pytest.mark.login
    @allure.severity(allure.severity_level.CRITICAL)
    def test_empty_password(self, login_page: LoginPage):
        """
        Test login with empty password.

        Steps:
        1. Enter valid username
        2. Leave password empty
        3. Click login
        4. Verify validation error

        Expected: Required field validation message
        """
        login_page.login(VALID_CREDENTIALS["username"], "")
        error_msg = login_page.get_error_message()
        assert error_msg, "Error message should be displayed"
        assert "Required" in error_msg or "password" in error_msg.lower() or "empty" in error_msg.lower()

    @pytest.mark.login
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_credentials(self, login_page: LoginPage):
        """
        Test login with both fields empty.

        Steps:
        1. Leave both fields empty
        2. Click login

        Expected: Validation messages for required fields
        """
        login_page.login("", "")
        error_msg = login_page.get_error_message()
        assert error_msg, "Error message should be displayed"

    @pytest.mark.login
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_page_elements(self, login_page: LoginPage):
        """
        Verify all login page elements are present.

        Steps:
        1. Navigate to login page
        2. Verify page elements exist

        Expected: Username field, Password field, Login button present
        """
        from pages.login_page import LoginPage
        assert login_page.is_element_present(LoginPage.USERNAME_INPUT), "Username input should be visible"
        assert login_page.is_element_present(LoginPage.PASSWORD_INPUT), "Password input should be visible"
        assert login_page.is_element_present(LoginPage.LOGIN_BUTTON), "Login button should be visible"

    @pytest.mark.login
    @allure.severity(allure.severity_level.MINOR)
    def test_login_page_loaded(self, login_page: LoginPage):
        """
        Test that login page is loaded correctly.

        Steps:
        1. Open login page
        2. Verify URL is correct
        3. Verify page title contains "Login"

        Expected: Login page is displayed with correct URL
        """
        assert "auth/login" in login_page.get_current_url().lower()
        assert login_page.is_on_login_page()

    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    def test_forgot_password_link(self, login_page: LoginPage):
        """
        Test navigation to forgot password page.

        Steps:
        1. Click "Forgot your password?" link
        2. Verify navigation to password reset page

        Expected: User is redirected to password reset page
        """
        login_page.click_forgot_password()
        current_url = login_page.get_current_url()
        assert "request-password-reset" in current_url.lower() or "forgot" in current_url.lower()

    @pytest.mark.logout
    def test_successful_logout(self, login_page: LoginPage):
        """
        Test logout functionality.

        Steps:
        1. Login successfully
        2. Click profile dropdown
        3. Click logout
        4. Verify redirected to login page

        Expected: User is logged out and back to login page
        """
        login_page.login(
            VALID_CREDENTIALS["username"],
            VALID_CREDENTIALS["password"]
        )
        assert login_page.is_login_successful()
        login_page.logout()
        assert login_page.is_on_login_page()


class TestOrangeHRMLoginDataDriven:
    """Data-driven tests for login functionality."""

    @pytest.mark.parametrize(
        "username,password,expected_error",
        [
            ("Admin", "admin123", "success"),
            ("wronguser", "admin123", "invalid"),
            ("admin", "admin123", "success"),
            ("", "admin123", "required"),
            ("Admin", "", "required"),
            ("", "", "required"),
            ("user!@#", "pass$%^", "invalid"),
            ("<script>", "pass", "invalid"),
            ("' OR 1=1 --", "pass", "invalid"),
        ],
        ids=[
            "Valid-Credentials",
            "Invalid-Username-Valid-Password",
            "Lowercase-Username",
            "Empty-Username",
            "Empty-Password",
            "Empty-Both-Fields",
            "Special-Chars-in-Credentials",
            "Script-Tags",
            "SQL-Injection-Attempt",
        ]
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_parametrized(self, login_page: LoginPage, username, password, expected_error):
        """
        Parametrized test for multiple login scenarios.

        Tests various combinations of usernames and passwords,
        including edge cases and potential security issues.
        """
        login_page.open()

        if expected_error == "success":
            login_page.login(username, password)
            try:
                assert login_page.is_login_successful(), "Should login successfully"
            except AssertionError:
                # If is_login_successful returns False but credentials are valid,
                # check for unexpected error
                pytest.fail(f"Valid credentials failed to login. URL: {login_page.get_current_url()}")
        else:
            login_page.login(username, password)
            error_msg = login_page.get_error_message()
            assert error_msg, f"Expected error message for scenario: {expected_error}"
