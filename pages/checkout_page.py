from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.first_name = (By.ID, "first-name")
        self.last_name = (By.ID, "last-name")
        self.postal_code = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.finish_button = (By.ID, "finish")
        self.complete_header = (By.CLASS_NAME, "complete-header")

    def enter_information(self, first, last, postal):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.first_name)
        ).send_keys(first)
        self.driver.find_element(*self.last_name).send_keys(last)
        self.driver.find_element(*self.postal_code).send_keys(postal)

    def continue_checkout(self):
        self.driver.find_element(*self.continue_button).click()

    def finish_checkout(self):
        self.driver.find_element(*self.finish_button).click()

    def is_order_complete(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.complete_header)
        ).text.lower() == "thank you for your order!"
