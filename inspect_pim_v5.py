"Get precise locators for search form and add employee form."

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
    wait.until(EC.presence_of_element_located((By.XPATH, "//h6[normalize-space()='Dashboard']")))
    time.sleep(1)

    # Go to employee list
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")
    time.sleep(5)
    print("=== EMPLOYEE LIST PAGE ===")
    print(f"URL: {driver.current_url}")

    # ALL filter inputs
    print("\n=== Filter Inputs (all visible inputs) ===")
    all_inputs = driver.find_elements(By.XPATH, "//input")
    for inp in all_inputs:
        try:
            if inp.is_displayed() and inp.get_attribute("type") not in ["hidden"]:
                itype = inp.get_attribute("type") or "text"
                iname = inp.get_attribute("name") or ""
                iph = inp.get_attribute("placeholder") or ""
                iclass = inp.get_attribute("class") or ""
                iclass = iclass[:60]
                # Check for "select-all"
                is_select_all = "select-all" in iclass or "checkbox" in iclass
                if not is_select_all:
                    print(f"  type='{itype}' name='{iname}' placeholder='{iph}' class='{iclass}'")
        except:
            pass

    # Try to type in first visible input
    print("\n=== Searching for name input ===")
    name_inputs = driver.find_elements(By.XPATH, "//input[@placeholder='Type for hints...']")
    print(f"  placeholder='Type for hints...': {len(name_inputs)}")

    # Employee id input likely next to label
    print("\n=== Filter label-input pairs ===")
    labels = driver.find_elements(By.XPATH, "//form//label")
    for lab in labels:
        try:
            if lab.is_displayed():
                label_text = lab.text.strip()
                if label_text:
                    print(f"  Label: '{label_text}'")
                    # find input after label
                    following = lab.find_elements(By.XPATH, ".//following-sibling::div//input")
                    for f_inp in following:
                        if f_inp.is_displayed():
                            print(f"    Input placeholder='{f_inp.get_attribute('placeholder')}' class='{f_inp.get_attribute('class')[:60]}'")
        except:
            pass

    # Checkboxes
    print("\n=== Checkboxes ===")
    check_inputs = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
    for cb in check_inputs:
        try:
            if cb.is_displayed():
                print(f"  class='{cb.get_attribute('class')[:60]}'")
                # Parent div info
                parent = cb.find_element(By.XPATH, "./ancestor::div[@class='oxd-table-cell oxd-table-cell--edit'][1]")
                print(f"    Parent: class exists")
        except:
            pass

    # Action buttons on row
    print("\n=== Action buttons (search entire row) ===")
    action_divs = driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-table-card-cell-')]")
    for ad in action_divs:
        try:
            buttons_in = ad.find_elements(By.XPATH, ".//button | .//a | .//div[@role='button']")
            if buttons_in and ad.is_displayed():
                print(f"  Parent div class: {ad.get_attribute('class')}")
                for b in buttons_in[:3]:
                    if b.is_displayed():
                        print(f"    btn class='{b.get_attribute('class')}'")
        except:
            pass

    # Try to find all SVGs/icons in rows
    print("\n=== SVG icons in table ===")
    svgs = driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-table-body')]//svg")
    print(f"  SVGs in table body: {len(svgs)}")
    for svg in svgs[:5]:
        try:
            parent = svg.find_element(By.XPATH, "./ancestor::button[1]")
            print(f"    Parent btn class: {parent.get_attribute('class')}")
        except:
            pass

    # ===== ADD EMPLOYEE PAGE =====
    print("\n\n=== ADD EMPLOYEE PAGE ===")
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee")
    time.sleep(3)

    # Name inputs
    for name in ["firstName", "middleName", "lastName"]:
        elems = driver.find_elements(By.NAME, name)
        if elems:
            e = elems[0]
            print(f"  {name}: value='{e.get_attribute('value')}' class='{e.get_attribute('class')[:60]}'")

    # employeeId
    eid_elements = driver.find_elements(By.NAME, "employeeId")
    if eid_elements:
        print(f"  employeeId: value='{eid_elements[0].get_attribute('value')}'")
    else:
        # Maybe not directly by name
        # Try to find by placeholder
        id_placeholder = driver.find_elements(By.XPATH, "//input[@placeholder='Employee Id']")
        print(f"  Input placeholder='Employee Id': {len(id_placeholder)}")
        if not id_placeholder:
            all_inputs = driver.find_elements(By.XPATH, "//input")
            for inp in all_inputs:
                try:
                    if inp.is_displayed() and inp.get_attribute("type") != "hidden":
                        v = inp.get_attribute("value")
                        ph = inp.get_attribute("placeholder")
                        n = inp.get_attribute("name")
                        print(f"    name='{n}' placeholder='{ph}' value='{v}' readonly='{inp.get_attribute('readonly')}'")
                except:
                    pass

    print("\n=== DONE ===")

finally:
    driver.quit()
