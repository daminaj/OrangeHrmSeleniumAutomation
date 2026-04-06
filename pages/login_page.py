"""
OrangeHRM Login Page Object Model.
URL: https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.settings import Settings


class LoginPage(BasePage):
    """Login Page with actions and validations."""

    # Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    DASHBOARD_HEADER = (By.XPATH, "//h6[normalize-space()='Dashboard']")
    ERROR_MESSAGE = (By.XPATH, "//p[contains(@class, 'oxd-alert-content')]")
    ERROR_MESSAGE_INLINE = (By.XPATH, "//span[@class='oxd-text oxd-text--span']")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//p[@class='oxd-text oxd-text--p orangehrm-login-forgot-header']")
    PROFILE_DROPDOWN = (By.XPATH, "//span[@class='oxd-userdropdown-tab']")
    LOGOUT_BUTTON = (By.LINK_TEXT, "Logout")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        """Navigate to login page."""
        from config.settings import Settings
        self.driver.get(Settings.BASE_URL)
        return self

    def enter_username(self, username):
        """Enter username."""
        return self.type_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        """Enter password."""
        return self.type_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        """Click login button."""
        return self.click(self.LOGIN_BUTTON)

    def login(self, username, password):
        """Perform login with credentials."""
        self.enter_username(username)
        self.enter_password(password)
        return self.click_login()

    def is_login_successful(self, timeout=None):
        """Check if login was successful (dashboard page is loaded).

        """
        if timeout is None:
            timeout = Settings.TIMEOUT + 10  # e.g., 20 seconds

        # Check current URL
        current_url = self.get_current_url()
        if "dashboard" not in current_url.lower():
            try:
                from selenium.common.exceptions import TimeoutException
                WebDriverWait(self.driver, 10).until(
                    lambda d: "dashboard" in d.current_url.lower()
                )
            except TimeoutException:
                return False

        # Wait for dashboard header (h6 containing Dashboard) to be visible
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: any(
                    el.is_displayed() and "dashboard" in el.text.lower()
                    for el in d.find_elements(By.TAG_NAME, "h6")
                )
            )
            return True
        except Exception:
            return False

    def get_error_message(self):
        """Get error message text after failed login attempt."""
        # Alert-style errors (e.g., "Invalid credentials")
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        # Inline validation errors (e.g., "Required")
        from selenium.webdriver.common.by import By
        validation_errors = self.driver.find_elements(
            By.XPATH,
            '//span[contains(@class, "oxd-text") and contains(text(), "Required")]',
        )
        for err in validation_errors:
            if err.is_displayed():
                return err.text
        # Fallback: any visible span with error text
        spans = self.driver.find_elements(By.TAG_NAME, "span")
        for sp in spans:
            try:
                if sp.is_displayed() and any(
                    kw in sp.text.lower()
                    for kw in ["required", "invalid", "error", "empty"]
                ):
                    return sp.text
            except Exception:
                continue
        return ""

    def is_on_login_page(self):
        """Check if currently on login page."""
        return (
            self.is_element_present(self.USERNAME_INPUT)
            and self.is_element_present(self.LOGIN_BUTTON)
            and "auth/login" in self.get_current_url()
        )

    def click_forgot_password(self):
        """Navigate to forgot password page."""
        return self.click(self.FORGOT_PASSWORD_LINK)

    def logout(self):
        """Perform logout if logged in."""
        if self.is_element_present(self.PROFILE_DROPDOWN):
            self.click(self.PROFILE_DROPDOWN)
            self.click(self.LOGOUT_BUTTON)
        return self
