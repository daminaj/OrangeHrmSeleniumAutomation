"""
OrangeHRM Admin Page Object.
Manages User Management under Admin section.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class AdminPage(BasePage):
    """Admin page with user management functionality."""

    # Admin page header
    ADMIN_HEADER = (By.XPATH, "//span[@class='oxd-topbar-header-breadcrumb']")
    USER_MENU_ITEM = (By.XPATH, "//span[normalize-space()='User Management']/..")
    USERS_SUBMENU_ITEM = (By.XPATH, "//span[normalize-space()='Users']/ancestor::a")

    # Search form
    USERNAME_SEARCH_INPUT = (
        By.XPATH,
        "//div[@class='oxd-input-group oxd-input-field-bottom-space']//div//input[@class='oxd-input oxd-input--active']"
    )
    # Role dropdown
    ROLE_DROPDOWN = (
        By.XPATH,
        "//body[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/form[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]"
    )
    ROLE_DROPDOWN_LIST = (
        By.XPATH,
        "//body[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/form[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]"
    )
    # Employee name
    EMPLOYEE_NAME_INPUT = (
        By.XPATH,
        "//input[@placeholder='Type for hints...']"
    )
    # Status dropdown
    STATUS_DROPDOWN = (
        By.XPATH,
        "//div[@class='oxd-table-filter-area']//div[2]//div[1]//div[2]//div[1]//div[1]//div[2]//i[1]"
    )
    STATUS_DROPDOWN_LIST = (
        By.XPATH,
        "//div[@role='listbox']//div[contains(@class, 'oxd-select-dropdown-item')]"
    )
    # Buttons
    SEARCH_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Search']"
    )
    RESET_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Reset']"
    )
    ADD_USER_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Add']"
    )

    # Search results table
    RESULTS_TABLE = (By.XPATH, "//div[contains(@class, 'oxd-table')]")
    TABLE_ROWS = (By.XPATH, "//div[@role='rowgroup']/div[contains(@class, 'oxd-table-row')]")
    TABLE_HEADER_CELLS = (
        By.XPATH,
        "//div[@role='rowgroup']/div[contains(@class, 'oxd-table-header')]"
    )

    # Pagination
    PAGINATION = (By.XPATH, "//*[contains(@class, 'oxd-table-pagination')]")
    PAGINATION_NEXT = (By.XPATH, "//i[contains(@class, 'oxd-icon') and contains(text(), 'chevron-right')]")

    # No records message
    NO_RECORDS_MESSAGE = (
        By.XPATH,
        "//*[contains(text(), 'No Records Found')]"
    )

    def __init__(self, driver):
        super().__init__(driver)

    def is_on_admin_page(self):
        """Verify we are on the Admin/User Management page."""
        return self.is_element_present(self.ADMIN_HEADER, timeout=10)

    def search_by_username(self, username):
        """Type text in username search field and click search."""
        if username:
            self.type_text(self.USERNAME_SEARCH_INPUT, username)
        self.click(self.SEARCH_BUTTON)
        return self

    def search_by_role(self, role):
        """Select role from dropdown and click search.

        Args:
            role: 'Admin', 'ESS', or similar
        """
        self.click(self.ROLE_DROPDOWN)
        role_option = (
            By.XPATH,
            f"//div[@role='listbox']//div[contains(text(), '{role}')]"
        )
        self.click(role_option)
        self.click(self.SEARCH_BUTTON)
        return self

    def search_by_status(self, status):
        """Select status from dropdown and click search.

        Args:
            status: 'Enabled', 'Disabled'
        """
        self.click(self.STATUS_DROPDOWN)
        status_option = (
            By.XPATH,
            f"//div[@role='listbox']//div[contains(text(), '{status}')]"
        )
        self.click(status_option)
        self.click(self.SEARCH_BUTTON)
        return self

    def reset_search(self):
        """Click reset button to clear filters."""
        self.click(self.RESET_BUTTON)
        return self

    def get_search_results(self):
        """Extract text from all rows in search results.

        Returns:
            List of dictionaries with column header -> cell value.
        """
        if not self.is_element_present(self.NO_RECORDS_MESSAGE):
            rows = self.find_elements(self.TABLE_ROWS)
            headers = self._get_column_headers()
            results = []
            for row in rows:
                cells = row.find_elements(By.XPATH, ".//div[contains(@class, 'oxd-table-cell')]")
                row_data = {}
                for idx, cell in enumerate(cells):
                    if idx < len(headers):
                        row_data[headers[idx]] = cell.text
                if row_data:
                    results.append(row_data)
            return results
        return []

    def get_user_count(self):
        """Get number of users returned from search."""
        if self.is_element_present(self.NO_RECORDS_MESSAGE, timeout=5):
            return 0
        rows = self.find_elements(self.TABLE_ROWS)
        return len(rows)

    def has_results(self):
        """Check if search returned any results."""
        return self.get_user_count() > 0

    def get_search_error_message(self):
        """Get 'No Records Found' message if displayed."""
        if self.is_element_present(self.NO_RECORDS_MESSAGE, timeout=5):
            return self.get_text(self.NO_RECORDS_MESSAGE)
        return ""

    def is_pagination_available(self):
        """Check if pagination controls are visible (implies many results)."""
        return self.is_element_present(self.PAGINATION)

    def click_add_user(self):
        """Click Add button to open add user form."""
        self.click(self.ADD_USER_BUTTON)
        return self

    def is_add_user_form_visible(self):
        """Verify the add user form is displayed."""
        return self.is_element_present(
            (By.XPATH, "//h6[normalize-space()='Add User']"), timeout=10
        )

    def get_add_user_form_fields(self):
        """Verify all expected form fields are present on add user page.

        Returns:
            Dictionary of field_name -> True if present
        """
        fields = {
            "User Role": self.is_element_present(
                (By.XPATH, "//label[normalize-space()='User Role']/following-sibling::div")
            ),
            "Employee Name": self.is_element_present(
                (By.XPATH, "//label[normalize-space()='Employee Name']/following-sibling::div")
            ),
            "Username": self.is_element_present(
                (By.XPATH, "//label[normalize-space()='Username']/following-sibling::div")
            ),
            "Password": self.is_element_present(
                (By.XPATH, "//label[normalize-space()='Password']/following-sibling::div")
            ),
            "Confirm Password": self.is_element_present(
                (By.XPATH, "//label[normalize-space()='Confirm Password']/following-sibling::div")
            ),
            "Status": self.is_element_present(
                (By.XPATH, "//label[normalize-space()='Status']/following-sibling::div")
            ),
            "Save Button": self.is_element_present(
                (By.XPATH, "//button[contains(text(), 'Save')]")
            ),
            "Cancel Button": self.is_element_present(
                (By.XPATH, "//button[contains(text(), 'Cancel')]")
            ),
        }
        return fields

    def click_cancel(self):
        """Click Cancel button on add user form."""
        self.click((By.XPATH, "//button[contains(text(), 'Cancel')]"))
        return self

    def _get_column_headers(self):
        """Extract column header labels from the table."""
        try:
            headers = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'oxd-table-header')]//div[contains(@class, 'oxd-table-cell')]"
            )
            return [h.text for h in headers if h.text]
        except Exception:
            return []
