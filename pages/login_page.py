from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.saucedemo.com/"
        self.username_input = (By.ID, "user-name")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.error_message = (By.CSS_SELECTOR, "h3[data-test='error']")  # for potential error validations
    
    def load(self):
        self.driver.get(self.url)
    
    def enter_username(self, username):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.username_input)
        ).clear()
        self.driver.find_element(*self.username_input).send_keys(username)
    
    def enter_password(self, password):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_input)
        ).clear()
        self.driver.find_element(*self.password_input).send_keys(password)
    
    def click_login(self):
        self.driver.find_element(*self.login_button).click()
    
    def get_error_message(self):
        # Returns error message text if present, else None
        try:
            error = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.error_message)
            )
            return error.text
        except:
            return None
