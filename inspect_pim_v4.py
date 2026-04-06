"Add employee and inspect table on PIM page."

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
    time.sleep(1)
    driver.find_element(By.TAG_NAME, "button").click()

    # Wait for dashboard
    wait.until(EC.presence_of_element_located((By.XPATH, "//h6[normalize-space()='Dashboard']")))
    time.sleep(1)
    print("Logged in.")

    # Navigate to Add Employee via URL (bypass side nav issues)
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee")
    time.sleep(3)
    print("On Add Employee page.")
    print(f"URL: {driver.current_url}")

    # Check fields on add page
    print("\n=== Add Employee Fields ===")
    fn = driver.find_elements(By.NAME, "firstName")
    mn = driver.find_elements(By.NAME, "middleName")
    ln = driver.find_elements(By.NAME, "lastName")
    eid = driver.find_elements(By.NAME, "employeeId")
    print(f"  firstName: {len(fn)}, middleName: {len(mn)}, lastName: {len(ln)}, employeeId: {len(eid)}")
    if eid:
        print(f"    employeeId value: {eid[0].get_attribute('value')}")
    if fn and mn and ln:
        fn[0].send_keys("TestEmpV4")
        ln[0].send_keys("LastNameV4")

    # Save
    driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()
    time.sleep(5)

    # Check toast
    toasts = driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-toast-container')]")
    if toasts:
        for toast in toasts:
            if toast.is_displayed():
                print(f"  Toast: '{toast.text}'")

    print(f"URL after save: {driver.current_url}")
    time.sleep(2)

    # Now navigate to employee list
    print("\n=== Navigating to Employee List ===")
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")
    time.sleep(5)
    print(f"URL: {driver.current_url}")

    # All inputs
    print("\n=== Search Form Inputs ===")
    all_inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
    print(f"  Text inputs: {len(all_inputs)}")
    for inp in all_inputs:
        try:
            if inp.is_displayed():
                print(f"    placeholder='{inp.get_attribute('placeholder')}' class='{inp.get_attribute('class')[:80]}'")
        except:
            pass

    # Check for checkbox
    checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
    print(f"\n  Checkboxes: {len(checkboxes)}")
    for cb in checkboxes[:3]:
        try:
            if cb.is_displayed():
                parent = cb.find_element(By.XPATH, "./ancestor::div[@class='oxd-table-card-cell-checkbox']")
                print(f"    class='oxd-table-card-cell-checkbox' found")
        except:
            pass

    # Table row count
    print("\n=== Table Structure ===")
    rows = driver.find_elements(By.XPATH, "//div[@role='rowgroup']/div[contains(@class,'oxd-table-row') and not(contains(@class,'header'))]")
    print(f"  Data rows: {len(rows)}")

    # Get header cells
    headers = driver.find_elements(By.XPATH, "//div[1]/div[contains(@class,'oxd-table')]/div[1]/div[1]//div[contains(@class,'oxd-table-cell')]")
    if not headers:
        headers = driver.find_elements(By.XPATH, "//div[2]//div[contains(@class,'oxd-table-header')]//div[contains(@class,'oxd-table-cell')]")

    print(f"  Header cells: {len(headers)}")
    for i, h in enumerate(headers):
        if h.is_displayed():
            print(f"  [{i}] '{h.text}'")

    # Try to find all spans in body
    print("\n=== Table body content ===")
    body_spans = driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-table-body')]//span")
    print(f"  Spans in body: {len(body_spans)}")
    for i, s in enumerate(body_spans[:15]):
        if s.is_displayed():
            print(f"    [{i}] '{s.text}'")

    # Action buttons
    print("\n=== Action buttons ===")
    for action_class in ['oxd-icon-button-pencil', 'oxd-icon-button-trash', 'oxd-icon-button-eye']:
        buttons = driver.find_elements(By.XPATH, f"//button[contains(@class,'{action_class}')]")
        print(f"  {action_class}: {len(buttons)}")
        if buttons:
            print(f"    href/onclick: class='{buttons[0].get_attribute('class')}'")

    # Checkboxes (all)
    all_cbs = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
    print(f"\n  Total checkboxes: {len(all_cbs)}")
    for cb in all_cbs[:5]:
        try:
            if cb.is_displayed():
                cb_class = cb.get_attribute('class')
                print(f"    class='{cb_class[:60]}' checked='{cb.is_selected()}'")
                # Check for select-all
                if 'select-all' in cb_class:
                    print("      ^^ SELECT ALL CHECKBOX ^^")
        except:
            pass

    # Pagination
    print("\n=== Pagination ===")
    pagination_elements = driver.find_elements(By.XPATH, "//*[contains(@class,'oxd-pagination')]")
    print(f"  Pagination: {len(pagination_elements)}")
    for p in pagination_elements:
        if p.is_displayed():
            print(f"  Pagination text: '{p.text[:100]}'")

    print("\n=== DONE ===")

finally:
    driver.quit()
