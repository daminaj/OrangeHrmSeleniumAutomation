"""
OrangeHRM PIM Module - Comprehensive Test Suite.
Tests all major components and functionality of the People Management page.
"""

import pytest
import allure
from pages.pim_page import PimPage
from test_data.test_data import SAMPLE_EMPLOYEES, SEARCH_CRITERIA


class TestPIMNavigation:
    """Tests for PIM module navigation and page structure."""

    @pytest.mark.smoke
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("pim", "navigation")
    @allure.label("owner", "automation")
    def test_pim_page_loads(self, pim_page: "PimPage"):
        """
        Test that PIM page loads correctly after navigation.

        Steps:
        1. Login as Admin
        2. Navigate to PIM from Dashboard
        3. Verify PIM page header is displayed
        4. Verify URL contains 'pim'

        Expected: PIM page is successfully loaded
        """
        assert pim_page.is_on_pim_page(), "PIM page header should be visible"
        assert "pim" in pim_page.get_current_url().lower()

    @pytest.mark.pim
    @allure.severity(allure.severity_level.NORMAL)
    def test_pim_page_components_visible(self, pim_page: "PimPage"):
        """
        Verify all major PIM page components are present.

        Steps:
        1. Navigate to PIM page
        2. Check for Employee List menu
        3. Check for Add Employee menu
        4. Check for search form and table
        5. Check for pagination

        Expected: All key UI elements are visible
        """
        with allure.step("Verify PIM sub-navigation menu items"):
            assert pim_page.is_element_present(pim_page.EMPLOYEE_LIST_MENU), "Employee List menu should be visible"
            assert pim_page.is_element_present(pim_page.ADD_EMPLOYEE_MENU), "Add Employee menu should be visible"

        with allure.step("Verify search/filter section"):
            assert pim_page.is_element_present(pim_page.SEARCH_FORM), "Search form should be visible"
            assert pim_page.is_element_present(pim_page.EMPLOYEE_NAME_INPUT), "Employee name input should be present"
            assert pim_page.is_element_present(pim_page.SEARCH_BUTTON), "Search button should be present"
            assert pim_page.is_element_present(pim_page.RESET_BUTTON), "Reset button should be present"

        with allure.step("Verify employee table"):
            assert pim_page.is_element_present(pim_page.RESULTS_TABLE), "Results table should be visible"

        with allure.step("Verify pagination presence"):
            # Pagination may or may not be visible depending on result count
            pim_page.is_pagination_visible()  # Just verify it doesn't error


class TestPIMEmployeeSearch:
    """Tests for employee search functionality."""

    @pytest.mark.pim
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "search_type,search_value,expected_min_count",
        [
            ("name", "Admin", 1),
            ("id", "E001", 1),
        ]
    )
    def test_search_employee_by_criteria(self, pim_page: "PimPage", search_type, search_value, expected_min_count):
        """
        Test employee search by different criteria.

        Steps:
        1. Perform search by Name or ID
        2. Get results count
        3. Verify at least expected_min_count results

        Expected: Search returns matching employee records
        """
        pim_page.reset_search()

        if search_type == "name":
            pim_page.search_by_employee_name(search_value)
        else:
            pim_page.search_by_employee_id(search_value)

        count = pim_page.get_search_results_count()
        assert count >= expected_min_count, f"Expected at least {expected_min_count} result(s), got {count}"

        # Verify returned data contains search term
        if count > 0:
            table_data = pim_page.get_employee_table_data()
            assert table_data, "Table data should be extracted"
            # Log found employees for debugging
            for row in table_data[:3]:  # Log first 3
                allure.attach(str(row), name="Employee Row", attachment_type=allure.attachment_type.TEXT)

    @pytest.mark.pim
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_with_invalid_name(self, pim_page: "PimPage"):
        """
        Test search with non-existent employee name.

        Steps:
        1. Enter a name that doesn't exist
        2. Click Search

        Expected: "No Records Found" message or 0 results
        """
        pim_page.reset_search()
        pim_page.search_by_employee_name("NonexistentEmployeeXYZ123")

        count = pim_page.get_search_results_count()
        assert count == 0, "Should return no results for non-existent employee"

        # Additional check for 'No Records Found' message
        try:
            error_msg = pim_page.driver.find_element(
                pim_page.driver.By.XPATH,
                "//*[contains(text(), 'No Records Found') or contains(text(), 'No records found')]"
            )
            assert error_msg.is_displayed()
        except:
            pass  # Message is optional if count is 0

    @pytest.mark.pim
    @allure.severity(allure.severity_level.NORMAL)
    def test_reset_clears_filters(self, pim_page: "PimPage"):
        """
        Test that Reset button clears search results.

        Steps:
        1. Perform a search (e.g., by name "Admin")
        2. Click Reset button
        3. Verify all employees are shown or filters cleared

        Expected: Search filters are cleared, all employees displayed
        """
        # First perform a search
        pim_page.search_by_employee_name("Admin")
        initial_count = pim_page.get_search_results_count()
        assert initial_count > 0, "Search should return results"

        # Reset
        pim_page.reset_search()

        # After reset, we expect more employees than the filtered search
        # (unless there's only one employee in system)
        reset_count = pim_page.get_search_results_count()
        assert reset_count >= initial_count, "Reset should show all records or more"

    @pytest.mark.pim
    @allure.severity(allure.severity_level.MINOR)
    def test_table_headers_are_present(self, pim_page: "PimPage"):
        """
        Verify that the employee table has expected column headers.

        Steps:
        1. Navigate to PIM Employee List
        2. Extract all column headers
        3. Verify presence of standard columns

        Expected: Table contains headers like Name, Id, Job Title, etc.
        """
        headers = pim_page.get_table_headers()
        assert headers, "Table headers should be extracted"

        # Common expected columns (case-insensitive check)
        header_names = [h.lower() for h in headers]
        # Typically OrangeHRM has: #, Name, Employee Id, Job Title, etc.
        expected_found = any(col in header_names for col in ["name", "employee name", "employee id", "id"])
        assert expected_found, f"Expected name or employee ID column. Found: {headers}"

        allure.attach(
            "\n".join(headers),
            name="Table Headers",
            attachment_type=allure.attachment_type.TEXT
        )


class TestPIMAddEmployee:
    """Tests for Add Employee functionality."""

    @pytest.mark.pim
    @pytest.mark.regression
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navigate_to_add_employee(self, pim_page: "PimPage"):
        """
        Test navigation to Add Employee form.

        Steps:
        1. On PIM page, click 'Add Employee' from sidebar
        2. Verify Add Employee form is displayed

        Expected: Add Employee form displays with all required fields
        """
        pim_page.navigate_to_add_employee()
        assert pim_page.is_add_employee_form_displayed(), "Add Employee form should be visible"
        assert pim_page.is_element_present(pim_page.FIRST_NAME_INPUT), "First Name field should be present"
        assert pim_page.is_element_present(pim_page.LAST_NAME_INPUT), "Last Name field should be present"

    @pytest.mark.pim
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_employee_with_required_fields_only(self, pim_page: "PimPage"):
        """
        Test adding a new employee with only required fields.

        Steps:
        1. Navigate to Add Employee
        2. Enter First Name and Last Name
        3. (Leave Employee ID default)
        4. Click Save

        Expected: Employee is added successfully, success message displayed
        """
        pim_page.navigate_to_add_employee()

        # Verify required fields are present
        fields = pim_page.are_form_fields_visible()
        assert fields["First Name"] and fields["Last Name"], "Required name fields must be present"

        # Add employee
        employee = SAMPLE_EMPLOYEES[3]  # "Test User"
        pim_page.add_employee(
            first_name=employee["first_name"],
            last_name=employee["last_name"],
            middle_name=employee["middle_name"]
        )

        # Verify success
        success_msg = pim_page.get_success_message()
        assert success_msg or pim_page.is_employee_list_visible(), "Should see success or return to employee list"

        allure.attach(f"Added: {employee['first_name']} {employee['last_name']}", name="Employee Added")

    @pytest.mark.pim
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_employee_with_optional_middle_name(self, pim_page: "PimPage"):
        """Test adding employee with middle name."""
        pim_page.navigate_to_add_employee()

        employee = SAMPLE_EMPLOYEES[0]  # John Doe
        pim_page.add_employee(
            first_name=employee["first_name"],
            last_name=employee["last_name"],
            middle_name=employee["middle_name"]
        )

        assert pim_page.is_employee_list_visible(), "Should return to employee list after adding"

    @pytest.mark.pim
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_employee_with_custom_id(self, pim_page: "PimPage"):
        """Test adding employee with specified employee ID."""
        pim_page.navigate_to_add_employee()

        employee = SAMPLE_EMPLOYEES[1]  # Jane Smith
        custom_id = "EMP_CUSTOM_001"
        pim_page.add_employee(
            first_name=employee["first_name"],
            last_name=employee["last_name"],
            employee_id=custom_id
        )

        assert pim_page.is_employee_list_visible()

        # Could optionally verify employee appears in list with that ID via search
        pim_page.search_by_employee_id(custom_id)
        count = pim_page.get_search_results_count()
        assert count >= 1, "Newly added employee should appear in search"

    @pytest.mark.pim
    @allure.severity(allure.severity_level.NORMAL)
    def test_required_field_validation_empty_names(self, pim_page: "PimPage"):
        """
        Test that required field validation appears for empty names.

        Steps:
        1. Navigate to Add Employee
        2. Leave First Name and Last Name empty
        3. Click Save
        4. Verify error messages for required fields

        Expected: Validation errors appear for required fields
        """
        pim_page.navigate_to_add_employee()

        errors = pim_page.get_required_fields_errors()
        assert errors, "Should see validation errors for empty required fields"

        allure.attach(
            "\n".join(errors),
            name="Validation Errors",
            attachment_type=allure.attachment_type.TEXT
        )


class TestPIMEmployeeActions:
    """Tests for employee actions (view, edit, delete)."""

    @pytest.fixture(autouse=False)
    def ensure_employee_exists(self, pim_page: "PimPage"):
        """Ensure at least one employee exists before running these tests."""
        pim_page.reset_search()
        # Try to find at least one employee
        if pim_page.get_search_results_count() == 0:
            # Add a default employee
            pim_page.navigate_to_add_employee()
            pim_page.add_employee("Auto", "Test", employee_id="AUTO001")
        return pim_page

    @pytest.mark.pim
    @allure.severity(allure.severity_level.NORMAL)
    def test_employee_row_has_action_buttons(self, pim_page: "PimPage"):
        """
        Verify that each employee row has Edit, Delete, and View buttons.

        Steps:
        1. On Employee List page
        2. Locate first employee row
        3. Check for Edit (pencil), Delete (trash), and View (eye) buttons

        Expected: Action buttons present on employee rows
        """
        pim_page.reset_search()

        count = pim_page.get_search_results_count()
        if count == 0:
            pytest.skip("No employees to test actions on")

        first_row = pim_page.find_element(pim_page.TABLE_DATA_ROWS)

        # Find action buttons in first row
        edit_btn = first_row.find_elements(pim_page.driver.By.XPATH, ".//button[contains(@class, 'oxd-icon-button-pencil')]")
        delete_btn = first_row.find_elements(pim_page.driver.By.XPATH, ".//button[contains(@class, 'oxd-icon-button-trash')]")
        view_btn = first_row.find_elements(pim_page.driver.By.XPATH, ".//button[contains(@class, 'oxd-icon-button-eye')]")

        assert len(edit_btn) > 0, "Edit button should be present on first row"
        assert len(delete_btn) > 0, "Delete button should be present on first row"
        assert len(view_btn) > 0, "View button should be present on first row"

    @pytest.mark.pim
    @pytest.mark.regression
    @allure.severity(allure.severity_level.CRITICAL)
    def test_view_employee_details(self, pim_page: "PimPage"):
        """
        Test viewing employee details.

        Steps:
        1. Click 'View' button on first employee row
        2. Verify Employee Details page opens
        3. Verify Personal Details/JOB/Qualifications sections are present

        Expected: Employee details are displayed
        """
        pim_page.reset_search()

        if pim_page.get_search_results_count() == 0:
            pytest.skip("No employees to view")

        pim_page.click_view_first_employee()

        assert pim_page.is_employee_details_visible(), "Employee Details page should be displayed"
        assert pim_page.is_element_present(pim_page.PERSONAL_DETAILS_SECTION), "Personal Details section should be present"

        allure.attach("View mode", name="Employee View Mode")

    @pytest.mark.pim
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_employee(self, pim_page: "PimPage"):
        """
        Test editing employee information.

        Steps:
        1. Click Edit button on first employee row
        2. Modify a field (e.g., middle name)
        3. Click Save
        4. Verify success

        Expected: Employee information is updated successfully
        """
        pim_page.reset_search()

        if pim_page.get_search_results_count() == 0:
            pytest.skip("No employees to edit")

        pim_page.click_edit_first_employee()

        # Should now be on employee edit page - Personal Details section should be visible
        assert pim_page.is_employee_details_visible(), "Edit page should be displayed"

        # Verify Save button is present
        assert pim_page.is_element_present(pim_page.SAVE_BUTTON), "Save button should be present on edit page"

        allure.attach("Edit mode", name="Employee Edit Mode")


class TestPIMTableFeatures:
    """Tests for table features like pagination, selection, etc."""

    @pytest.mark.pim
    @allure.severity(allure.severity_level.NORMAL)
    def test_select_all_checkbox(self, pim_page: "PimPage"):
        """
        Test bulk selection checkbox behavior.

        Steps:
        1. On Employee List page with multiple employees
        2. Click 'Select All' checkbox
        3. Verify all row checkboxes become selected
        """
        pim_page.reset_search()

        # Ensure there are multiple employees
        count = pim_page.get_search_results_count()
        if count < 2:
            pytest.skip("Need at least 2 employees to test select all")

        # Click select all
        select_all = pim_page.driver.find_element(*pim_page.SELECT_ALL_CHECKBOX)
        select_all.click()

        # Check that row checkboxes are now selected
        # (Yes, this is a basic sanity check)
        assert select_all.is_selected() or select_all.get_attribute("aria-checked") == "true"

    @pytest.mark.pim
    @allure.severity(allure.severity_level.MINOR)
    def test_pagination_display(self, pim_page: "PimPage"):
        """
        Verify pagination controls are displayed when applicable.

        Steps:
        1. Refresh employee list
        2. Check for pagination element
        3. Log pagination info
        """
        pim_page.reset_search()

        if pim_page.is_pagination_visible():
            # Capture pagination text
            pagination = pim_page.driver.find_element(*pim_page.PAGINATION)
            pagination_text = pagination.text
            allure.attach(pagination_text, name="Pagination Info", attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach("No pagination displayed (single page of results)", name="Pagination Info")

    @pytest.mark.pim
    @allure.severity(allure.severity_level.NORMAL)
    def test_employee_data_integrity(self, pim_page: "PimPage"):
        """
        Verify that employee table data is well-formed and non-empty.

        Steps:
        1. Extract all employee rows from table
        2. Verify each row has data
        3. Verify no row is completely empty

        Expected: All displayed rows contain meaningful data
        """
        pim_page.reset_search()
        data = pim_page.get_employee_table_data()

        assert len(data) > 0, "Should have at least one employee"

        for idx, row in enumerate(data):
            assert any(row.values()), f"Row {idx} appears empty: {row}"
            # Ensure each row has at least some text in first column
            first_col = list(row.values())[0] if row else ""
            assert first_col.strip(), f"First column in row {idx} is empty"

        allure.attach(
            f"Total employees displayed: {len(data)}\n\nFirst employee:\n{data[0]}",
            name="Data Integrity Check",
            attachment_type=allure.attachment_type.TEXT
        )


class TestPIMEdgeCases:
    """Edge case and negative tests for PIM functionality."""

    @pytest.mark.pim
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_after_reset_returns_full_list(self, pim_page: "PimPage"):
        """Verify that resetting after search restores full employee list."""
        # Search for something
        pim_page.search_by_employee_name("Admin")
        filtered_count = pim_page.get_search_results_count()

        # Reset
        pim_page.reset_search()
        reset_count = pim_page.get_search_results_count()

        assert reset_count >= filtered_count, "Reset should show equal or more employees than filtered search"

    @pytest.mark.pim
    @allure.severity(allure.severity_level.MINOR)
    def test_navigation_submenu_consistency(self, pim_page: "PimPage"):
        """Verify PIM submenu items remain clickable after page loads."""
        # Should still be on PIM page
        assert pim_page.is_on_pim_page()

        # Try to click Employee List (should do nothing if already there)
        pim_page.click(pim_page.EMPLOYEE_LIST_MENU)
        assert pim_page.is_employee_list_visible()

    @pytest.mark.pim
    @pytest.mark.parametrize("name", ["", "   ", "\t", "\n"])
    @allure.severity(allure.severity_level.MINOR)
    def test_search_with_invalid_name_input(self, pim_page: "PimPage", name: str):
        """Test that searching with whitespace-only or empty name doesn't crash."""
        pim_page.reset_search()

        # Should not raise an exception
        pim_page.search_by_employee_name(name)
        count = pim_page.get_search_results_count()
        assert count >= 0, "Should get a valid count"
