"""Diagnostic script to inspect OrangeHRM PIM page structure."""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
# options.add_argument("--headless=new")  # Run with UI to see what's happening
options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

try:
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.TAG_NAME, "button").click()

    # Wait for dashboard
    wait.until(EC.presence_of_element_located((By.XPATH, "//h6[normalize-space()='Dashboard']")))
    print("Logged in. Navigating to PIM...")

    # Click PIM using the same locator as DashboardPage
    pim_link = driver.find_element(By.XPATH, "//span[normalize-space()='PIM']/ancestor::a")
    pim_link.click()
    time.sleep(5)

    print("=== URL ===")
    print(driver.current_url)

    print("\n=== Page title ===")
    print(driver.title)

    # Check for headers
    print("\n=== H1-H6 headers ===")
    for h in driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4 | //h5 | //h6"):
        if h.is_displayed():
            print(f"  {h.tag_name}: '{h.text}'")

    # Search form
    print("\n=== Search/Filter Form Elements ===")
    form = driver.find_elements(By.XPATH, "//form")
    if form:
        print("  Found form(s)")
        # Look for inputs by placeholder
        for placeholder in ["Name", "Id", "Employee Name", "Employee Id", "Job Title", "Location", "Include"]:
            elems = driver.find_elements(By.XPATH, f"//input[@placeholder='{placeholder}']")
            if elems:
                print(f"  Input with placeholder='{placeholder}': {len(elems)}")
        # Look for dropdowns via class or structure
        selects = driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-select')]")
        print(f"  oxd-select dropdowns: {len(selects)}")
        # Buttons
        for btn_text in ["Search", "Reset", "Add"]:
            btns = driver.find_elements(By.XPATH, f"//button[normalize-space()='{btn_text}']")
            print(f"  Button '{btn_text}': {len(btns)}")

    # Table
    print("\n=== Table Structure ===")
    tables = driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-table')]")
    print(f"  oxd-table count: {len(tables)}")
    # Header cells
    headers = driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-table-header')]//div[contains(@class,'oxd-table-cell')]")
    for h in headers:
        if h.is_displayed():
            print(f"  HEADER: '{h.text}'")
    # Data rows
    rows_v1 = driver.find_elements(By.XPATH, "//div[@role='rowgroup']/div[contains(@class,'oxd-table-row')]")
    rows_v2 = driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-table-body')]/div[contains(@class,'oxd-table-row')]")
    print(f"  rowgroup rows: {len(rows_v1)}, oxd-table-body rows: {len(rows_v2)}")
    # Row cells
    if rows_v1:
        cells = rows_v1[0].find_elements(By.XPATH, ".//div[contains(@class,'oxd-table-cell')]")
        print(f"    First row cell count: {len(cells)}")
        for i, c in enumerate(cells):
            print(f"      [{i}] '{c.text[:50].strip()}'")

    # Action buttons in rows
    print("\n=== Row Action Buttons (Edit/Delete/View) ===")
    if rows_v1:
        first_row = rows_v1[0]
        for icon_class in ['oxd-icon-button-pencil', 'oxd-icon-button-trash', 'oxd-icon-button-eye']:
            icons = first_row.find_elements(By.XPATH, f".//button[contains(@class,'{icon_class}')]")
            print(f"  {icon_class}: {len(icons)}")

    # Pagination
    print("\n=== Pagination ===")
    pagination = driver.find_elements(By.XPATH, "//*[contains(@class,'oxd-pagination')]")
    print(f"  Pagination components: {len(pagination)}")
    if pagination:
        print("  Text:", pagination[0].text[:200])

    # 'Add' button
    print("\n=== Add Employee ===")
    add_btns = driver.find_elements(By.XPATH, "//button[normalize-space()='Add']")
    print(f"  'Add' buttons: {len(add_btns)}")

    # Employee Name input in filter
    print("\n=== Employee Name input check ===")
    name_inputs = driver.find_elements(By.XPATH, "//input[@placeholder='Type for hints...']")
    print(f"  Input with placeholder 'Type for hints...': {len(name_inputs)}")
    # Employee ID input in filter
    id_inputs = driver.find_elements(By.XPATH, "//input[@name='employeeId']")
    print(f"  Input with name='employeeId': {len(id_inputs)}")

    # If no direct employeeId input, maybe different name
    all_inputs = driver.find_elements(By.XPATH, "//form//input")
    print(f"\n  Total form inputs: {len(all_inputs)}")
    for inp in all_inputs:
        try:
            name = inp.get_attribute("name")
            placeholder = inp.get_attribute("placeholder")
            if name or placeholder:
                print(f"    name='{name}' placeholder='{placeholder}'")
        except:
            pass

    print("\n=== DONE ===")

finally:
    driver.quit()
