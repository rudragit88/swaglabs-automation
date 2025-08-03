from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.saucedemo.com/cart.html"
        self.cart_items_locator = (By.CLASS_NAME, "cart_item")
        self.cart_product_names_locator = (By.CLASS_NAME, "inventory_item_name")
        self.checkout_button_locator = (By.ID, "checkout")
        self.empty_cart_message_locator = (By.CLASS_NAME, "cart_empty")  # Adjust if your page uses another class for "empty" state

    def load(self):
        """
        Navigate to the cart page directly.
        """
        self.driver.get(self.url)
    
    def is_loaded(self, timeout=10):
        """
        Wait for the cart page to be loaded.
        Returns True if cart items present; returns False otherwise (e.g., empty cart).
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.cart_items_locator)
            )
            return True
        except TimeoutException:
            return False

    def get_cart_products(self):
        """
        Get a list of all product names present in the cart.
        Returns an empty list if no products.
        """
        try:
            products = self.driver.find_elements(*self.cart_product_names_locator)
            return [p.text for p in products]
        except NoSuchElementException:
            return []

    def is_cart_empty(self):
        """
        Return True if cart is empty by checking for a known 'empty' message or no products present.
        Adjust locator/class if your site uses a different marker for empty carts.
        """
        try:
            empty_msg = self.driver.find_element(*self.empty_cart_message_locator)
            return empty_msg.is_displayed()
        except NoSuchElementException:
            products = self.get_cart_products()
            return len(products) == 0

    def click_checkout(self):
        """
        Click the Checkout button to proceed with purchase.
        """
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.checkout_button_locator)
        ).click()
