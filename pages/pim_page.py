"""
OrangeHRM PIM (People Management) Page Object.
URL: https://opensource-demo.orangehrmlive.com/web/index.php/pim
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class PimPage(BasePage):
    """PIM module page with employee management functionality."""

    # --- Page Header & Navigation ---
    PIM_HEADER = (By.XPATH, "//h6[normalize-space()='PIM']")
    ADD_EMPLOYEE_HEADER = (By.XPATH, "//h6[normalize-space()='Add Employee']")
    EMPLOYEE_LIST_HEADER = (By.XPATH, "//h5[normalize-space()='Employee Information']")

    # --- Employee List Page - Search/Filter Section ---
    # Employee Name input (first occurrence with placeholder Type for hints...)
    EMPLOYEE_NAME_INPUT = (By.XPATH, "//input[@placeholder='Type for hints...'][1]")
    # General search box
    GENERAL_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search']")

    # Search/Reset buttons
    SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    RESET_BUTTON = (By.XPATH, "//button[normalize-space()='Reset']")

    # Add Employee button
    ADD_EMPLOYEE_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")

    # --- Employee List Table ---
    RESULTS_TABLE = (By.XPATH, "//div[@class='orangehrm-container']")

    # Table header cells (first row of header)
    TABLE_HEADER_ROW = (By.XPATH, "//div[@role='rowgroup']/div[contains(@class,'oxd-table-header')]")
    # Each header cell text
    TABLE_HEADER_CELLS = (By.XPATH, "//div[@role='rowgroup']/div[contains(@class,'oxd-table-header')]//div[contains(@class,'oxd-table-cell')]")

    # Data rows (not header)
    TABLE_DATA_ROWS = (By.XPATH, "//div[@role='rowgroup']/div[contains(@class,'oxd-table-row') and not(contains(@class,'header'))]")

    # Table cell content
    # Each row contains multiple cells; we can find cells within a row
    TABLE_CELLS = (By.XPATH, ".//div[@role='cell']")

    # Checkbox for selecting rows
    SELECT_ALL_CHECKBOX = (By.XPATH, "//div[@role='columnheader']//label")
    ROW_CHECKBOX = (By.XPATH, ".//div[contains(@class,'oxd-table-cell')]//input[@type='checkbox']")

    # Action buttons - in the edit column (pencil, trash, eye)
    # These are inside the last cell of each row (with class oxd-table-cell--edit)
    EDIT_BUTTON = (By.XPATH, ".//div[contains(@class,'oxd-table-cell--edit')]//button[contains(@class,'pencil') or contains(@class,'edit')]")
    DELETE_BUTTON = (By.XPATH, ".//div[contains(@class,'oxd-table-cell--edit')]//button[contains(@class,'trash') or contains(@class,'delete')]")
    VIEW_BUTTON = (By.XPATH, ".//div[contains(@class,'oxd-table-cell--edit')]//button[contains(@class,'eye') or contains(@class,'view')]")

    # --- Add Employee Form ---
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    MIDDLE_NAME_INPUT = (By.NAME, "middleName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    # Employee ID is auto-generated (readonly), so we don't normally set it
    EMPLOYEE_ID_DISPLAY = (By.XPATH, "//label[normalize-space()='Employee Id']/following-sibling::div//input | //input[contains(@class,'oxd-input') and @readonly]")

    # Create Login Details toggle
    CREATE_LOGIN_DETAILS_TOGGLE = (By.XPATH, "//span[@class='oxd-switch-input oxd-switch-input--active --label-right']")
    LOGIN_USERNAME_INPUT = (By.NAME, "username")
    LOGIN_PASSWORD_INPUT = (By.XPATH, "//input[@type='password' and @placeholder='Password']")
    CONFIRM_PASSWORD_INPUT = (By.XPATH, "//input[@type='password' and @placeholder='Confirm Password']")

    # Status dropdown (if needed - typically "Enabled" by default)
    STATUS_DROPDOWN = (By.XPATH, "//div[contains(@class,'oxd-select-wrapper')]")
    # Save & Cancel
    SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Save']")
    CANCEL_BUTTON = (By.XPATH, "//a[normalize-space()='Cancel']")

    # Success & Error messages
    SUCCESS_TOAST = (By.XPATH, "//div[contains(@class,'oxd-toast--success')]//div[contains(@class,'oxd-toast-content')]")
    ERROR_TOAST = (By.XPATH, "//div[contains(@class,'oxd-toast--error')]//div[contains(@class,'oxd-toast-content')]")

    # --- Employee Details Page (view/edit) ---
    EMPLOYEE_DETAILS_HEADER = (By.XPATH, "//h6[normalize-space()='Employee Details']")
    PERSONAL_DETAILS_SECTION = (By.XPATH, "//h6[normalize-space()='Personal Details']")
    JOB_DETAILS_SECTION = (By.XPATH, "//h6[normalize-space()='Job']")
    QUALIFICATIONS_SECTION = (By.XPATH, "//h6[normalize-space()='Qualifications']")
    MEMBERSHIPS_SECTION = (By.XPATH, "//h6[normalize-space()='Memberships']")

    # --- No Records ---
    NO_RECORDS_MESSAGE = (By.XPATH, "//*[contains(text(), 'No') and contains(text(), 'Records')]")

    def __init__(self, driver):
        super().__init__(driver)

    # ==================== Navigation ====================

    def open(self):
        """Navigate to PIM Employee List page."""
        from config.settings import Settings
        base = Settings.BASE_URL.replace('/auth/login', '')
        self.driver.get(f"{base}/pim/viewEmployeeList")
        return self

    def is_on_pim_page(self):
        """Verify PIM page is loaded."""
        return self.is_element_present(self.PIM_HEADER, timeout=10)

    def is_employee_list_visible(self):
        """Check if Employee List view is displayed."""
        return self.is_element_present(self.TABLE_DATA_ROWS) or self.is_element_present(self.RESULTS_TABLE)

    def navigate_to_add_employee(self):
        """Click Add Employee button."""
        self.click(self.ADD_EMPLOYEE_BUTTON)
        return self

    def is_add_employee_form_displayed(self):
        """Check if Add Employee form is visible."""
        return self.is_element_present(self.ADD_EMPLOYEE_HEADER, timeout=10)

    # ==================== Employee Search ====================

    def search_by_employee_name(self, name):
        """Search by employee name."""
        if name:
            self.type_text(self.EMPLOYEE_NAME_INPUT, name)
        self.click(self.SEARCH_BUTTON)
        return self

    def search_by_general(self, term):
        """Use general search box."""
        if term:
            self.type_text(self.GENERAL_SEARCH_INPUT, term)
        self.click(self.SEARCH_BUTTON)
        return self

    def reset_search(self):
        """Click Reset to clear filters."""
        self.click(self.RESET_BUTTON)
        return self

    def get_search_results_count(self):
        """Get number of employee rows displayed."""
        if self.is_element_present(self.NO_RECORDS_MESSAGE, timeout=3):
            return 0
        rows = self.find_elements(self.TABLE_DATA_ROWS)
        return len(rows)

    def has_search_results(self):
        """Check if any employee records are returned."""
        return self.get_search_results_count() > 0

    def get_table_headers(self):
        """Extract all column header names."""
        headers = []
        try:
            header_elements = self.driver.find_elements(*self.TABLE_HEADER_CELLS)
            headers = [h.text.strip() for h in header_elements if h.text.strip()]
        except Exception as e:
            print(f"Error getting headers: {e}")
        return headers

    def get_employee_table_data(self):
        """Extract all employee data from the table as list of dicts."""
        headers = self.get_table_headers()
        rows = self.find_elements(self.TABLE_DATA_ROWS)
        data = []

        for row in rows:
            cells = row.find_elements(By.XPATH, ".//div[@role='cell']")
            row_dict = {}
            for idx, cell in enumerate(cells):
                if idx < len(headers):
                    row_dict[headers[idx]] = cell.text.strip()
            if row_dict:
                data.append(row_dict)
        return data

    def get_first_employee_name(self):
        """Get the name of the first employee."""
        data = self.get_employee_table_data()
        if data:
            for col in ["Name", "Employee Name", "Full Name", "First Name"]:
                if col in data[0]:
                    return data[0][col]
        return None

    def is_pagination_visible(self):
        """Check if pagination is visible."""
        return self.is_element_present((By.XPATH, "//*[contains(@class,'oxd-pagination')]"))

    # ==================== Add Employee ====================

    def fill_employee_name(self, first_name, last_name, middle_name=""):
        """Enter name fields."""
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.MIDDLE_NAME_INPUT, middle_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        return self

    def get_employee_id_from_form(self):
        """Get the auto-generated employee ID (after save or from form)."""
        try:
            eid_element = self.driver.find_element(*self.EMPLOYEE_ID_DISPLAY)
            return eid_element.get_attribute("value")
        except:
            return ""

    def save_employee(self):
        """Click Save button on add/edit form."""
        self.click(self.SAVE_BUTTON)
        # Wait for either success toast or navigation
        try:
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located(self.SUCCESS_TOAST),
                    EC.presence_of_element_located(self.EMPLOYEE_DETAILS_HEADER),
                    EC.presence_of_element_located(self.EMPLOYEE_LIST_HEADER)
                )
            )
        except:
            pass
        return self

    def add_employee(self, first_name, last_name, middle_name="", create_login=False, username="", password=""):
        """
        Add a new employee.

        Args:
            first_name, last_name: Required
            middle_name: Optional
            create_login: Boolean - create login credentials
            username, password: Required if create_login=True
        """
        # Navigate to Add Employee if needed
        if not self.is_add_employee_form_displayed():
            self.navigate_to_add_employee()

        # Fill name fields
        self.fill_employee_name(first_name, last_name, middle_name)

        # Optional login details
        if create_login:
            self.click(self.CREATE_LOGIN_DETAILS_TOGGLE)
            self.type_text(self.LOGIN_USERNAME_INPUT, username)
            self.type_text(self.LOGIN_PASSWORD_INPUT, password)
            self.type_text(self.CONFIRM_PASSWORD_INPUT, password)

        # Save
        self.save_employee()
        return self

    def get_success_message(self):
        """Get success toast message."""
        if self.is_element_present(self.ERROR_TOAST):
            return ""
        if self.is_element_present(self.SUCCESS_TOAST):
            return self.get_text(self.SUCCESS_TOAST)
        return ""

    # ==================== Employee Row Actions ====================

    def select_first_employee(self):
        """Select checkbox for first employee row."""
        try:
            first_row = self.find_element(self.TABLE_DATA_ROWS)
            checkbox = first_row.find_element(By.XPATH, ".//input[@type='checkbox']")
            checkbox.click()
        except Exception as e:
            print(f"Could not select first employee: {e}")
        return self

    def click_edit_first_employee(self):
        """Click Edit button on first employee row."""
        try:
            first_row = self.find_element(self.TABLE_DATA_ROWS)
            edit_btn = first_row.find_element(By.XPATH, ".//div[contains(@class,'oxd-table-cell--edit')]//button[1]")
            edit_btn.click()
        except Exception as e:
            print(f"Could not click edit: {e}")
        return self

    def click_delete_first_employee(self):
        """Click Delete button on first employee row."""
        try:
            first_row = self.find_element(self.TABLE_DATA_ROWS)
            delete_btn = first_row.find_element(By.XPATH, ".//div[contains(@class,'oxd-table-cell--edit')]//button[2]")
            delete_btn.click()
        except Exception as e:
            print(f"Could not click delete: {e}")
        return self

    def click_view_first_employee(self):
        """Click View button on first employee row."""
        try:
            first_row = self.find_element(self.TABLE_DATA_ROWS)
            view_btn = first_row.find_element(By.XPATH, ".//div[contains(@class,'oxd-table-cell--edit')]//button[3]")
            view_btn.click()
        except Exception as e:
            print(f"Could not click view: {e}")
        return self

    def is_employee_details_visible(self):
        """Check if employee details page is displayed."""
        return self.is_element_present(self.EMPLOYEE_DETAILS_HEADER, timeout=5)

    def are_form_fields_visible(self):
        """Check that required Add Employee fields are present."""
        fields = {
            "First Name": self.is_element_present(self.FIRST_NAME_INPUT),
            "Middle Name": self.is_element_present(self.MIDDLE_NAME_INPUT),
            "Last Name": self.is_element_present(self.LAST_NAME_INPUT),
            "Save": self.is_element_present(self.SAVE_BUTTON),
            "Cancel": self.is_element_present(self.CANCEL_BUTTON),
        }
        return fields

    def get_required_fields_errors(self):
        """Attempt to submit empty form and collect validation errors."""
        errors = []
        try:
            # Try clicking save without required fields
            self.click(self.SAVE_BUTTON)
            # Look for "Required" messages
            error_elements = self.driver.find_elements(
                By.XPATH,
                "//span[contains(@class,'oxd-text') and contains(text(),'Required')]"
            )
            errors = [el.text for el in error_elements if el.is_displayed()]
        except:
            pass
        return errors
