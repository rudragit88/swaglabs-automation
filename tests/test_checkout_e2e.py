import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


@pytest.fixture
def driver():
    service = Service()
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_checkout_e2e_valid(driver):
    login_page = LoginPage(driver)
    login_page.load()
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()

    inventory_page = InventoryPage(driver)
    inventory_page.is_loaded()
    products_to_buy = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]

    # Add products to cart with synchronization on badge count        
    for index, product in enumerate(products_to_buy, start=1):
        print(f"Attempting to add product: '{product}'")
        added = inventory_page.add_product_to_cart(product)
        assert added, f"Failed to add product '{product}' to cart"

        # Wait until the cart badge count equals current number of added products
        def badge_matches(_):
            try:
                count = inventory_page.get_cart_badge_count()
                print(f"Waiting for cart badge to be {index}, currently: {count}")
                return count == index
            except (StaleElementReferenceException, NoSuchElementException):
                return False

        WebDriverWait(driver, 20).until(badge_matches)

    # Go to cart and verify both products are listed
    cart_page = CartPage(driver)
    cart_page.load()
    cart_page.is_loaded()
    cart_products = cart_page.get_cart_products()
    for product in products_to_buy:
        assert product in cart_products

    # Start checkout using new Selenium4+ locator style
    driver.find_element(By.ID, "checkout").click()

    checkout_page = CheckoutPage(driver)
    checkout_page.enter_information("John", "Doe", "10001")
    checkout_page.continue_checkout()

    # Verify product summary (optional)
    summary_products = [
        elem.text for elem in driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    ]
    for product in products_to_buy:
        assert product in summary_products

    # Finish checkout
    checkout_page.finish_checkout()
    assert checkout_page.is_order_complete()

    # Cart badge should disappear (cart empty)
    time.sleep(1)  # Allow UI to update
    assert inventory_page.get_cart_badge_count() == 0

    # Optional: Confirm cart is empty after checkout
    cart_page.load()
    cart_page.is_loaded()
    assert cart_page.get_cart_products() == []
