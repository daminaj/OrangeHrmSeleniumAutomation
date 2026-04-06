"""Diagnostic script to inspect OrangeHRM PIM page after adding employee."""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

try:
    # Login
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.TAG_NAME, "button").click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//h6[normalize-space()='Dashboard']")))
    print("Logged in. Navigating to PIM...")

    # Click PIM
    driver.find_element(By.XPATH, "//span[normalize-space()='PIM']/ancestor::a").click()
    time.sleep(3)

    # Click Add Employee
    print("Clicking Add Employee button...")
    add_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Add']")
    add_btn.click()
    time.sleep(2)

    # Fill form
    print("Filling employee form...")
    driver.find_element(By.NAME, "firstName").send_keys("Test")
    driver.find_element(By.NAME, "lastName").send_keys("Employee")
    # Click Save
    driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()
    time.sleep(3)

    # After save, should be back on employee list
    print("Back to employee list. Taking 5 sec to load...")
    time.sleep(5)

    print("\n=== URL ===")
    print(driver.current_url)

    print("\n=== H1-H6 headers ===")
    for h in driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4 | //h5 | //h6"):
        if h.is_displayed():
            print(f"  {h.tag_name}: '{h.text}'")

    # Search form
    print("\n=== Search/Filter Form ===")
    # Employee Name input
    name_inputs = driver.find_elements(By.XPATH, "//input[@placeholder='Type for hints...']")
    print(f"  Name input count: {len(name_inputs)}")
    if name_inputs:
        print(f"    placeholder: {name_inputs[0].get_attribute('placeholder')}")
        print(f"    class: {name_inputs[0].get_attribute('class')[:80]}")

    # Employee ID input (likely has different placeholder or label)
    id_inputs = driver.find_elements(By.XPATH, "//input[@placeholder='Id']")
    print(f"  ID input with placeholder='Id': {len(id_inputs)}")
    if not id_inputs:
        # Try by label
        id_labels = driver.find_elements(By.XPATH, "//label[normalize-space()='Employee Id']")
        print(f"  Label 'Employee Id': {len(id_labels)}")
        if id_labels:
            # Following sibling or parent structure
            following = id_labels[0].find_elements(By.XPATH, ".//following-sibling::div//input")
            print(f"    Following sibling input: {len(following)}")
            parent_div = id_labels[0].find_element(By.XPATH, "./..")
            all_inputs_in_parent = parent_div.find_elements(By.XPATH, ".//input")
            print(f"    Inputs in same parent div: {len(all_inputs_in_parent)}")
            for inp in all_inputs_in_parent:
                print(f"      - input placeholder: {inp.get_attribute('placeholder')}, name: {inp.get_attribute('name')}")

    # Buttons
    search_btns = driver.find_elements(By.XPATH, "//button[normalize-space()='Search']")
    reset_btns = driver.find_elements(By.XPATH, "//button[normalize-space()='Reset']")
    add_btns = driver.find_elements(By.XPATH, "//button[normalize-space()='Add']")
    print(f"  Buttons - Search: {len(search_btns)}, Reset: {len(reset_btns)}, Add: {len(add_btns)}")

    # Table
    print("\n=== Table Structure ===")
    tables = driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-table')]")
    print(f"  oxd-table count: {len(tables)}")

    # Header cells
    headers = driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-table-header')]//div[contains(@class,'oxd-table-cell')]")
    print(f"  Header cell count: {len(headers)}")
    header_texts = []
    for h in headers:
        if h.is_displayed():
            txt = h.text.strip()
            if txt:
                header_texts.append(txt)
                print(f"    '{txt}'")
    print(f"  Headers: {header_texts}")

    # Data rows - alternative XPath
    rows = driver.find_elements(By.XPATH, "//div[@role='rowgroup']/div[contains(@class,'oxd-table-row')]")
    print(f"  Rows (rowgroup): {len(rows)}")
    if len(rows) == 0:
        # Try another structure
        rows2 = driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-table-body')]/div[contains(@class,'oxd-table-row')]")
        print(f"  Rows (oxd-table-body): {len(rows2)}")
        rows = rows2 if rows2 else rows

    if rows:
        # Get cells from first row
        cells = rows[0].find_elements(By.XPATH, ".//div[contains(@class,'oxd-table-cell')]")
        print(f"    First row cell count: {len(cells)}")
        for i, cell in enumerate(cells):
            print(f"      [{i}] '{cell.text.strip()}'")

        # Check for action buttons inside row
        print("\n    Action buttons in first row:")
        edit_btns = rows[0].find_elements(By.XPATH, ".//button[contains(@class,'oxd-icon-button-pencil')]")
        del_btns = rows[0].find_elements(By.XPATH, ".//button[contains(@class,'oxd-icon-button-trash')]")
        view_btns = rows[0].find_elements(By.XPATH, ".//button[contains(@class,'oxd-icon-button-eye')]")
        print(f"      Edit (pencil): {len(edit_btns)}")
        print(f"      Delete (trash): {len(del_btns)}")
        print(f"      View (eye): {len(view_btns)}")

        # Checkboxes
        checkboxes = rows[0].find_elements(By.XPATH, ".//input[@type='checkbox']")
        print(f"      Checkboxes: {len(checkboxes)}")

    # Pagination
    print("\n=== Pagination ===")
    pagination = driver.find_elements(By.XPATH, "//*[contains(@class,'oxd-pagination')]")
    print(f"  Pagination components: {len(pagination)}")

    print("\n=== DONE ===")

finally:
    driver.quit()
