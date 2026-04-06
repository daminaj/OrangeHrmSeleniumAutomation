"""Inspect PIM page structure and print all relevant elements."""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless=new")
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

    # Wait for dashboard
    wait.until(EC.presence_of_element_located((By.XPATH, "//h6[normalize-space()='Dashboard']")))
    print("Logged in. Navigating to PIM...")

    # Click PIM
    driver.find_element(By.XPATH, "//span[normalize-space()='PIM']/ancestor::a").click()
    time.sleep(5)

    print("\n=== URL ===")
    print(driver.current_url)

    print("\n=== Page title ===")
    print(driver.title)

    # Check for header
    print("\n=== H1/H5/H6 headers on page ===")
    for h in driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4 | //h5 | //h6"):
        if h.is_displayed():
            print(f"  {h.tag_name}: '{h.text}'")

    # All text inputs
    print("\n=== Input fields ===")
    for inp in driver.find_elements(By.TAG_NAME, "input"):
        try:
            if inp.is_displayed():
                attrs = {"type": inp.get_attribute("type"), "name": inp.get_attribute("name"),
                         "placeholder": inp.get_attribute("placeholder"), "class": inp.get_attribute("class")[:80]}
                print(f"  {attrs}")
        except:
            pass

    # All buttons
    print("\n=== Buttons ===")
    for btn in driver.find_elements(By.TAG_NAME, "button"):
        try:
            if btn.is_displayed():
                print(f"  '{btn.text}' class='{btn.get_attribute('class')[:60]}'")
        except:
            pass

    # Anchor menu items
    print("\n=== Sidebar menu items ===")
    for a in driver.find_elements(By.XPATH, "//aside//a[contains(@class, 'oxd-main-menu-item')]"):
        try:
            if a.is_displayed():
                print(f"  '{a.text.strip()}' href='{a.get_attribute('href')}'")
        except:
            pass

    # Table rows
    print("\n=== Table row count ===")
    rows = driver.find_elements(By.XPATH, "//div[@role='row']")
    print(f"  Total row elements: {len(rows)}")
    for r in rows[:3]:
        print(f"  Row text: '{r.text[:100]}'")

    # Table header cells
    print("\n=== Table header cells ===")
    headers = driver.find_elements(By.XPATH, "//div[contains(@class, 'oxd-table-header')]//div[contains(@class, 'oxd-table-cell')]")
    for h in headers:
        if h.is_displayed():
            print(f"  '{h.text}'")

    # Check for search form area
    print("\n=== Search form area ===")
    search_area = driver.find_elements(By.XPATH, "//div[contains(@class, 'oxd-table-filter-area')]")
    if search_area:
        print("  Found oxd-table-filter-area")
        for child in search_area[0].find_elements(By.XPATH, ".//*"):
            try:
                if child.is_displayed() and child.text.strip():
                    print(f"    {child.tag_name}: '{child.text.strip()}'")
            except:
                pass

    # No records found message
    print("\n=== Messages ===")
    for msg in driver.find_elements(By.XPATH, "//*[contains(text(), 'No Records') or contains(text(), 'No records')]"):
        print(f"  '{msg.text}'")

    # Try pagination
    print("\n=== Pagination ===")
    pagination = driver.find_elements(By.XPATH, "//*[contains(@class, 'oxd-pagination')]")
    print(f"  Found: {len(pagination)} elements")

finally:
    driver.quit()
