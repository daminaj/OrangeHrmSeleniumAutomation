"""
Pytest configuration and fixtures.
"""

import pytest
from utils.driver_manager import DriverManager
from config.settings import Settings
from test_data.test_data import VALID_CREDENTIALS


def pytest_configure(config):
    """Configure pytest before tests."""
    # Ensure reports directory exists
    import os
    os.makedirs("reports/allure", exist_ok=True)
    os.makedirs("reports/html", exist_ok=True)

    # Allure configuration
    config.option.allure_report_dir = "reports/allure"


@pytest.fixture(scope="function")
def driver():
    """
    WebDriver fixture for each test.

    Initializes fresh browser per test, cleans up after.
    """
    driver = DriverManager.init_driver()
    driver.maximize_window()

    yield driver

    DriverManager.quit_driver()


@pytest.fixture(scope="function")
def login_page(driver):
    """LoginPage fixture that opens the login page."""
    from pages.login_page import LoginPage
    page = LoginPage(driver)
    page.open()
    return page


@pytest.fixture(scope="function")
def dashboard_page(driver):
    """DashboardPage fixture - logs in and returns dashboard."""
    from pages.login_page import LoginPage
    from pages.dashboard_page import DashboardPage
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(
        VALID_CREDENTIALS["username"],
        VALID_CREDENTIALS["password"]
    )
    assert login_page.is_login_successful()
    return DashboardPage(driver)


@pytest.fixture(scope="function")
def admin_page(driver):
    """AdminPage fixture - logs in, goes to dashboard, then Admin."""
    from pages.login_page import LoginPage
    from pages.dashboard_page import DashboardPage
    from pages.admin_page import AdminPage
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(
        VALID_CREDENTIALS["username"],
        VALID_CREDENTIALS["password"]
    )
    assert login_page.is_login_successful()
    dashboard = DashboardPage(driver)
    dashboard.navigate_to_admin()
    return AdminPage(driver)


@pytest.fixture(scope="function")
def pim_page(driver):
    """PimPage fixture - logs in and navigates to PIM module."""
    from pages.login_page import LoginPage
    from pages.dashboard_page import DashboardPage
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(
        VALID_CREDENTIALS["username"],
        VALID_CREDENTIALS["password"]
    )
    assert login_page.is_login_successful()
    dashboard = DashboardPage(driver)
    return dashboard.navigate_to_pim()

