"""Test data for OrangeHRM tests."""

# Login credentials
VALID_CREDENTIALS = {"username": "Admin", "password": "admin123"}

LOGIN_TEST_DATA = [
    ("Admin", "admin123", "success"),
    ("wronguser", "admin123", "invalid"),
    ("admin", "admin123", "success"),
    ("", "admin123", "required"),
    ("Admin", "", "required"),
    ("", "", "required"),
    ("user!@#", "pass$%^", "invalid"),
    ("<script>", "pass", "invalid"),
    ("' OR 1=1 --", "pass", "invalid"),
]

EDGE_CASE_DATA = [
    ("admin", "admin123"),
    ("ADMIN", "ADMIN123"),
    ("  Admin  ", "admin123"),
    ("Admin", "admin123  "),
]

# PIM/Employee data
SAMPLE_EMPLOYEES = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "employee_id": "E001",
        "middle_name": ""
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "employee_id": "E002",
        "middle_name": "Marie"
    },
    {
        "first_name": "Robert",
        "last_name": "Johnson",
        "employee_id": "E003",
        "middle_name": "James"
    },
    {
        "first_name": "Test",
        "last_name": "User",
        "employee_id": "E999",
        "middle_name": ""
    },
]

SEARCH_CRITERIA = [
    {"name": "John", "expected_count": 1},
    {"name": "Smith", "expected_count": 1},
    {"id": "E001", "expected_count": 1},
    {"name": "Nonexistent", "expected_count": 0},
]