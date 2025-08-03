import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage

@pytest.fixture
def driver():
    service = Service()  # Add executable_path if chromedriver is not in PATH, e.g. Service('path/to/chromedriver')
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_valid_user_login(driver):
    login_page = LoginPage(driver)
    login_page.load()
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()

    # Wait until redirected to inventory page
    WebDriverWait(driver, 10).until(EC.url_contains("/inventory.html"))

    # Verify URL contains /inventory.html
    assert "/inventory.html" in driver.current_url, "Did not navigate to inventory page after login"

    # Verify the inventory page container is visible
    inventory_container = driver.find_element(By.ID, "inventory_container")
    assert inventory_container.is_displayed(), "Inventory container is not visible"
