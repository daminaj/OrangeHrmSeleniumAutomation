"""
Diagnostic script to inspect OrangeHRM login page structure.
"""

import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
# options.add_argument("--headless=new")  # Run with UI to see what's happening
options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

try:
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    print("Page title:", driver.title)
    print("URL:", driver.current_url)
    print()

    # Wait for page to load
    time.sleep(5)

    # Get full page source after JS loads
    print("=== Page source excerpt (first 3000 chars) ===")
    source = driver.page_source
    print(source[:3000])
    print()

    # Try to find all input elements
    print("=== All input elements on page ===")
    inputs = driver.find_elements(By.TAG_NAME, "input")
    for inp in inputs:
        try:
            attrs = {
                "tag": inp.tag_name,
                "type": inp.get_attribute("type"),
                "name": inp.get_attribute("name"),
                "placeholder": inp.get_attribute("placeholder"),
                "class": inp.get_attribute("class"),
                "id": inp.get_attribute("id"),
                "aria-label": inp.get_attribute("aria-label"),
            }
            # Filter None values
            attrs = {k: v for k, v in attrs.items() if v}
            print(attrs)
        except:
            pass
    print()

    # Try to find all buttons
    print("=== All button elements on page ===")
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for btn in buttons[:10]:
        try:
            attrs = {
                "type": btn.get_attribute("type"),
                "text": btn.text[:50],
                "class": btn.get_attribute("class"),
                "aria-label": btn.get_attribute("aria-label"),
            }
            attrs = {k: v for k, v in attrs.items() if v}
            print(attrs)
        except:
            pass
    print()

    # Check for specific div structure
    print("=== Looking for label/text near login ===")
    labels = driver.find_elements(By.TAG_NAME, "label")
    for lab in labels[:5]:
        print(f"Label text: {lab.text}")
    print()

finally:
    driver.quit()
