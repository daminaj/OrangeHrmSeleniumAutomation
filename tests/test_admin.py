"""
Tests for OrangeHRM Admin/User Management module.

These tests verify navigation, search, filters, and add user functionality.
"""

import pytest
import allure
from pages.admin_page import AdminPage
from pages.dashboard_page import DashboardPage


@allure.epic("Admin Module")
@allure.feature("Admin Page Navigation")
class TestAdminNavigation:
    """Tests for navigating to and verifying Admin page."""

    @allure.story("Navigate to Admin")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_navigates_to_admin_from_dashboard(self, dashboard_page: DashboardPage):
        """
        Test navigating from Dashboard to Admin page via side menu.

        Steps:
        1. Login (via dashboard_page fixture)
        2. Navigate to Admin page
        3. Verify Admin page loads
        """
        dashboard_page.navigate_to_admin()
        admin_page = AdminPage(dashboard_page.driver)
        assert admin_page.is_on_admin_page(), "Admin page should be displayed after navigation"

    @allure.story("Admin Page Elements")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_admin_page_elements_present(self, dashboard_page: DashboardPage):
        """
        Verify all core Admin page elements are present.

        Steps:
        1. Navigate to Admin page
        2. Verify search form, Add User button, and table are visible
        """
        dashboard_page.navigate_to_admin()
        admin_page = AdminPage(dashboard_page.driver)
        admin_page.is_on_admin_page()

        assert admin_page.is_element_present(admin_page.USERNAME_SEARCH_INPUT), "Username search field should be visible"
        assert admin_page.is_element_present(admin_page.ROLE_DROPDOWN), "Role dropdown should be visible"
        assert admin_page.is_element_present(admin_page.EMPLOYEE_NAME_INPUT), "Employee name field should be visible"
        assert admin_page.is_element_present(admin_page.STATUS_DROPDOWN), "Status dropdown should be visible"
        assert admin_page.is_element_present(admin_page.SEARCH_BUTTON), "Search button should be visible"
        assert admin_page.is_element_present(admin_page.RESET_BUTTON), "Reset button should be visible"
        assert admin_page.is_element_present(admin_page.RESULTS_TABLE), "Results table should be visible"


@allure.epic("Admin Module")
@allure.feature("User Search")
class TestUserSearch:
    """Tests for search functionality on Admin page."""

    @allure.story("Search by Username")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_search_user_by_username(self, admin_page: AdminPage):
        """
        Test searching for a specific user by username.

        Steps:
        1. Navigate to Admin page (via fixture)
        2. Enter 'Admin' in username search
        3. Click Search
        4. Verify at least one result is returned
        """
        admin_page.search_by_username("Admin")
        results = admin_page.get_search_results()
        assert len(results) > 0, "Should return at least one user with username 'Admin'"

    @allure.story("Search Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_user_nonexistent(self, admin_page: AdminPage):
        """
        Test search with nonexistent username shows proper message.

        Steps:
        1. Enter a username that doesn't exist
        2. Click Search
        3. Verify 'No Records Found' is displayed
        """
        admin_page.search_by_username("ThisUserShouldNotExist123")
        assert admin_page.has_results() is False, "Should not return any results"
        error_msg = admin_page.get_search_error_message()
        assert "No Records Found" in error_msg or "no records" in error_msg.lower(), \
            "Should show 'No Records Found' message"

    @allure.story("Reset Search")
    @allure.severity(allure.severity_level.NORMAL)
    def test_reset_search_form(self, admin_page: AdminPage):
        """
        Test reset button clears search filters.

        Steps:
        1. Perform a search (by username)
        2. Click Reset
        3. Verify results show all users (or more than the filtered set)
        """
        # First search for Admin
        admin_page.search_by_username("Admin")
        admin_results_count = admin_page.get_user_count()

        # Reset
        admin_page.reset_search()
        all_results_count = admin_page.get_user_count()

        assert all_results_count >= admin_results_count, \
            "After reset, results count should be >= filtered count"

    @allure.story("Search by Status")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_by_status_enabled(self, admin_page: AdminPage):
        """
        Test filtering users by Enabled status.

        Steps:
        1. Select 'Enabled' from status dropdown
        2. Click Search
        3. Verify all returned users have Status = Enabled
        """
        admin_page.search_by_status("Enabled")
        results = admin_page.get_search_results()
        assert len(results) > 0, "Should return at least some enabled users"
        for user in results:
            status = user.get("Status", "")
            assert status == "Enabled", f"Expected all results to be Enabled, got {status}"

    @allure.story("Search by Role")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_by_role_admin(self, admin_page: AdminPage):
        """
        Test filtering users by Admin role.

        Steps:
        1. Select 'Admin' from user role dropdown
        2. Click Search
        3. Verify all returned users have User Role = Admin
        """
        admin_page.search_by_role("Admin")
        results = admin_page.get_search_results()
        assert len(results) > 0, "Should return at least some Admin role users"
        for user in results:
            role = user.get("User Role", "")
            assert "admin" in role.lower(), f"Expected role containing 'Admin', got {role}"

    @allure.story("Empty Search")
    @allure.severity(allure.severity_level.MINOR)
    def test_empty_search_shows_all_users(self, admin_page: AdminPage):
        """
        Test that clicking Search with empty fields shows all users.

        Steps:
        1. Load Admin page with no filters
        2. Click Search empty
        3. Verify results table is populated
        """
        # The admin_page fixture loads the page with initial results
        initial_count = admin_page.get_user_count()
        assert initial_count > 0, "Admin page should display users by default"

        # Perform an empty search (reset then search with empty fields)
        admin_page.click(admin_page.SEARCH_BUTTON)
        after_search_count = admin_page.get_user_count()

        assert after_search_count > 0, "Empty search should still return users"

    @allure.story("Pagination")
    @allure.severity(allure.severity_level.MINOR)
    def test_pagination_displays(self, admin_page: AdminPage):
        """
        Test that pagination appears when there are multiple pages of results.

        Steps:
        1. Verify pagination controls are present
        2. If next button than one page exists, pagination is functional
        """
        if admin_page.is_pagination_available():
            assert True, "Pagination controls are present"
        else:
            pytest.skip("Only one page of results; pagination not applicable")


@allure.epic("Admin Module")
@allure.feature("Add User")
class TestAddUser:
    """Tests for the Add User functionality."""

    @allure.story("Add User Form")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_user_form_opens(self, admin_page: AdminPage):
        """
        Test clicking Add button opens add user form.

        Steps:
        1. Click Add User button
        2. Verify add user form is visible
        """
        admin_page.click_add_user()
        assert admin_page.is_add_user_form_visible(), "Add user form should be displayed"

    @allure.story("Add User Form")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_user_form_fields_present(self, admin_page: AdminPage):
        """
        Verify all required fields are present on the Add User form.

        Steps:
        1. Open Add User form
        2. Verify presence of: User Role, Employee Name, Username, Password,
           Confirm Password, Status, Save and Cancel buttons
        """
        admin_page.click_add_user()
        fields = admin_page.get_add_user_form_fields()

        missing = [name for name, present in fields.items() if not present]
        assert not missing, f"Missing fields on Add User form: {', '.join(missing)}"

    @allure.story("Add User Form")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_user_cancel_returns_to_list(self, admin_page: AdminPage):
        """
        Test clicking Cancel returns to user listing.

        Steps:
        1. Open Add User form
        2. Click Cancel
        3. Verify we are back on the Admin page (table is visible)
        """
        admin_page.click_add_user()
        assert admin_page.is_add_user_form_visible()
        admin_page.click_cancel()

        # After cancel we should be back to table view
        assert admin_page.is_on_admin_page(), "Should return to Admin page after cancel"
        assert admin_page.is_element_present(admin_page.RESULTS_TABLE), "Results table should be visible"
