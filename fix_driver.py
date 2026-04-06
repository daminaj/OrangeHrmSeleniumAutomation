"""Fix ChromeDriver by clearing cache and forcing fresh download."""

import os
import shutil
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Clear webdriver-manager cache
wdm_path = os.path.expanduser("~/.wdm")
if os.path.exists(wdm_path):
    print(f"Removing WDM cache: {wdm_path}")
    shutil.rmtree(wdm_path)
    print("Cache cleared.")
else:
    print("No WDM cache found.")

# Force fresh download
print("\nDownloading fresh ChromeDriver...")
try:
    driver_path = ChromeDriverManager().install()
    print(f"ChromeDriver installed at: {driver_path}")
except Exception as e:
    print(f"Error downloading driver: {e}")
    print("\nTry manually:")
    print("1. Check your Chrome version (chrome://settings/help)")
    print("2. Update webdriver-manager: pip install -U webdriver-manager")
    print("3. Or specify exact ChromeDriver version in DriverManager")
