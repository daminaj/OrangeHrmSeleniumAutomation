"""
Base Page Object with common functionality.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.settings import Settings


class BasePage:
    """Base page with common methods."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Settings.TIMEOUT)
        self.timeout = Settings.TIMEOUT

    def find_element(self, locator):
        """Find single element with explicit wait."""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise NoSuchElementException(f"Element not found: {locator}")

    def find_elements(self, locator):
        """Find all matching elements."""
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []

    def click(self, locator):
        """Click element with wait for clickability."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return self

    def type_text(self, locator, text):
        """Type text into an input field."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        return self

    def get_text(self, locator):
        """Get text from element."""
        return self.find_element(locator).text

    def is_element_present(self, locator, timeout=5):
        """Check if element is present."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def get_current_url(self):
        """Get current page URL."""
        return self.driver.current_url

    def get_page_title(self):
        """Get page title."""
        return self.driver.title

    def wait_for_page_to_load(self):
        """Wait for page to load completely."""
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return self

    def switch_to_default_content(self):
        """Switch back to default content (main frame)."""
        self.driver.switch_to.default_content()
        return self
