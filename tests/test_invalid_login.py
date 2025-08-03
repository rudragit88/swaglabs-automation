import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage

@pytest.fixture
def driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    
    # Initialize ChromeDriver (adjust executable_path if needed)
    service = Service()
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_invalid_credentials_login(driver):
    login_page = LoginPage(driver)
    login_page.load()
    
    # Enter invalid credentials
    login_page.enter_username("invalid_user")
    login_page.enter_password("wrong_password")
    login_page.click_login()

    # Wait for error message to be visible
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    ).text
    
    # Check if the error message is as expected
    assert "Username and password do not match any user in this service" in error_message
    
    # Verify URL is still the login page (no redirect)
    assert "saucedemo.com" in driver.current_url and "/inventory.html" not in driver.current_url
