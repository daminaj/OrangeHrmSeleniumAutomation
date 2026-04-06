"""
Configuration settings loaded from .env file.
Provides centralized access to all test configuration.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Test configuration settings."""

    BASE_URL = os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    BROWSER = os.getenv("BROWSER", "chrome").lower()
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", "10"))
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "5"))

    VALID_USERNAME = os.getenv("VALID_USERNAME", "Admin")
    VALID_PASSWORD = os.getenv("VALID_PASSWORD", "admin123")

    SELENIUM_HUB_URL = os.getenv("SELENIUM_HUB_URL", "")