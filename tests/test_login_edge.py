import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage

@pytest.fixture
def driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    service = Service()
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.mark.parametrize("username,password", [
    ("ab", "secret_sauce"),                  # Username too short
    ("a"*30, "secret_sauce"),                # Username too long
    ("standard_user", "12"),                 # Password too short
    ("standard_user", "a"*30),               # Password too long
    ("ab", "12"),                            # Both too short
    ("a"*30, "a"*30),                        # Both too long
])
def test_login_username_password_length_edge(driver, username, password):
    login_page = LoginPage(driver)
    login_page.load()
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login()

    # Wait for error message to appear and check
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    ).text

    assert "Username and password do not match any user in this service" in error_message

    # Assert that no redirect happened
    assert "/inventory.html" not in driver.current_url
