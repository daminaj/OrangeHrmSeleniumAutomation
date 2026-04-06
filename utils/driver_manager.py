"""
Thread-safe DriverManager for parallel test execution.
Supports local browser and Selenium Grid/Selenoid.
"""

import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config.settings import Settings


class DriverManager:
    """Thread-safe driver factory and manager."""

    _driver = threading.local()

    @classmethod
    def get_driver(cls):
        """Get the driver instance for current thread."""
        if not hasattr(cls._driver, "instance"):
            raise RuntimeError("WebDriver not initialized. Call init_driver() first.")
        return cls._driver.instance

    @classmethod
    def init_driver(cls):
        """Initialize WebDriver based on config."""
        browser = Settings.BROWSER
        headless = Settings.HEADLESS
        hub_url = Settings.SELENIUM_HUB_URL

        if hub_url:
            driver = cls._get_remote_driver(hub_url, browser, headless)
        elif browser == "chrome":
            driver = cls._get_chrome_driver(headless)
        elif browser == "firefox":
            driver = cls._get_firefox_driver(headless)
        else:
            driver = cls._get_chrome_driver(headless)

        cls._driver.instance = driver
        return cls._driver.instance

    @classmethod
    def _get_chrome_driver(cls, headless):
        """Create local Chrome driver."""
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    @classmethod
    def _get_firefox_driver(cls, headless):
        """Create local Firefox driver."""
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")

        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    @classmethod
    def _get_remote_driver(cls, hub_url, browser, headless):
        """Create Remote WebDriver (Grid/Selenoid)."""
        options = ChromeOptions() if browser == "chrome" else FirefoxOptions()
        if headless:
            options.add_argument("--headless=new")

        if browser == "chrome":
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        return webdriver.Remote(command_executor=hub_url, options=options)

    @classmethod
    def quit_driver(cls):
        """Quit driver and clean up thread-local storage."""
        if hasattr(cls._driver, "instance"):
            try:
                cls._driver.instance.quit()
            except Exception:
                pass
            delattr(cls._driver, "instance")
