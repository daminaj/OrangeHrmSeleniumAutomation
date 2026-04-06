"""
OrangeHRM Dashboard Page Object.
URL after login: https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Dashboard page with side navigation menu."""

    # Sidebar navigation
    SIDEBAR_MENU = (By.CLASS_NAME, "oxd-main-menu")
    ADMIN_MENU_ITEM = (By.XPATH, "//span[normalize-space()='Admin']/ancestor::a")
    PIM_MENU_ITEM = (By.XPATH, "//span[normalize-space()='PIM']/ancestor::a")
    LEAVE_MENU_ITEM = (By.XPATH, "//span[normalize-space()='Leave']/ancestor::a")
    TIME_MENU_ITEM = (By.XPATH, "//span[normalize-space()='Time']/ancestor::a")
    RECRUITMENT_MENU_ITEM = (By.XPATH, "//span[normalize-space()='Recruitment']/ancestor::a")
    MY_INFO_MENU_ITEM = (By.XPATH, "//span[normalize-space()='My Info']/ancestor::a")
    PERFORMANCE_MENU_ITEM = (By.XPATH, "//span[normalize-space()='Performance']/ancestor::a")
    DASHBOARD_MENU_ITEM = (By.XPATH, "//span[normalize-space()='Dashboard']/ancestor::a")
    DIRECTORY_MENU_ITEM = (By.XPATH, "//span[normalize-space()='Directory']/ancestor::a")
    MAINTENANCE_MENU_ITEM = (By.XPATH, "//span[normalize-space()='Maintenance']/ancestor::a")
    CLAIM_MENU_ITEM = (By.XPATH, "//span[normalize-space()='Claim']/ancestor::a")
    BUZZ_MENU_ITEM = (By.XPATH, "//span[normalize-space()='Buzz']/ancestor::a")

    # Dashboard header
    DASHBOARD_HEADER = (By.XPATH, "//h6[normalize-space()='Dashboard']")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        """Navigate to dashboard (typically after login)."""
        from config.settings import Settings
        self.driver.get(f"{Settings.BASE_URL.replace('/auth/login', '')}/dashboard/index")
        return self

    def is_on_dashboard(self):
        """Check if dashboard is loaded."""
        return self.is_element_present(self.DASHBOARD_HEADER)

    def navigate_to_admin(self):
        """Click Admin menu item to navigate to Admin page."""
        self.click(self.ADMIN_MENU_ITEM)
        return self

    def navigate_to_pim(self):
        """Click PIM menu item to navigate to PIM page."""
        from pages.pim_page import PimPage
        self.click(self.PIM_MENU_ITEM)
        return PimPage(self.driver)

    def get_all_menu_items(self):
        """Get dictionary of all main menu items (for exploratory purposes)."""
        return {
            "Admin": self.ADMIN_MENU_ITEM,
            "PIM": self.PIM_MENU_ITEM,
            "Leave": self.LEAVE_MENU_ITEM,
            "Time": self.TIME_MENU_ITEM,
            "Recruitment": self.RECRUITMENT_MENU_ITEM,
            "My Info": self.MY_INFO_MENU_ITEM,
            "Performance": self.PERFORMANCE_MENU_ITEM,
            "Dashboard": self.DASHBOARD_MENU_ITEM,
            "Directory": self.DIRECTORY_MENU_ITEM,
            "Maintenance": self.MAINTENANCE_MENU_ITEM,
            "Claim": self.CLAIM_MENU_ITEM,
            "Buzz": self.BUZZ_MENU_ITEM,
        }
