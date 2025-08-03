from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.saucedemo.com/inventory.html"
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
        self.inventory_container = (By.ID, "inventory_container")

    def is_loaded(self):
        """
        Waits until the inventory container is visible, confirming page load.
        """
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.inventory_container)
        )

    def add_product_to_cart(self, product_name):
        """
        Add product by name if 'Add to cart' button is present.
        Returns True if added, False if product already in cart.
        """
        products = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        for product in products:
            name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
            if name == product_name:
                button = product.find_element(By.TAG_NAME, "button")
                print(f"Add to Cart - Product: '{product_name}', Button Text: '{button.text}'")
                if button.text.lower() == "add to cart":
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(button))
                    button.click()
                    time.sleep(1)  # pause to allow UI update
                    return True
                else:
                    return False
        raise Exception(f"Product with name '{product_name}' not found.")

    def remove_product_from_cart(self, product_name):
        """
        Remove product by name if 'Remove' button is present.
        Returns True if removed, False if product not in cart.
        """
        products = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        for product in products:
            name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
            if name == product_name:
                button = product.find_element(By.TAG_NAME, "button")
                print(f"Remove from Cart - Product: '{product_name}', Button Text: '{button.text}'")
                if button.text.lower() == "remove":
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(button))
                    button.click()
                    time.sleep(1)  # pause to allow UI update
                    return True
                else:
                    return False
        raise Exception(f"Product with name '{product_name}' not found.")

    def get_cart_badge_count(self):
        """
        Returns current cart badge count as int or 0 if badge missing.
        """
        try:
            badge = self.driver.find_element(*self.cart_badge)
            count = int(badge.text)
            print(f"Current cart badge count: {count}")
            return count
        except NoSuchElementException:
            print("Cart badge not found; count is 0")
            return 0

    def get_add_button_text(self, product_name):
        """
        Gets 'Add to cart' or 'Remove' button text for product by name.
        """
        products = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        for product in products:
            name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
            if name == product_name:
                button_text = product.find_element(By.TAG_NAME, "button").text
                print(f"Button text for '{product_name}': '{button_text}'")
                return button_text
        raise Exception(f"Product with name '{product_name}' not found.")
