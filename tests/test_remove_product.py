import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture
def driver():
    service = Service()
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_remove_product_from_cart(driver):
    # Step 1: Login
    login_page = LoginPage(driver)
    login_page.load()
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()

    # Step 2: Wait for Inventory page
    inventory_page = InventoryPage(driver)
    inventory_page.is_loaded()

    product_name = "Sauce Labs Backpack"

    # Step 3: Add product if it isn't already added
    button_text = inventory_page.get_add_button_text(product_name)
    if button_text.lower() == "add to cart":
        inventory_page.add_product_to_cart(product_name)

    # Wait for cart badge count to be 1
    WebDriverWait(driver, 10).until(lambda d: inventory_page.get_cart_badge_count() == 1)
    assert inventory_page.get_cart_badge_count() == 1

    # Step 4: Remove the product (now using the correct method)
    removed = inventory_page.remove_product_from_cart(product_name)
    assert removed, "Failed to remove the product from cart"

    # Step 5: Wait until cart badge count becomes 0 or badge disappears robustly
    def cart_badge_zero(driver):
        try:
            count = inventory_page.get_cart_badge_count()
            print(f"Waiting for cart badge count to be zero. Current: {count}")
            return count == 0
        except StaleElementReferenceException:
            return False

    WebDriverWait(driver, 15).until(cart_badge_zero)
    assert inventory_page.get_cart_badge_count() == 0

    # Step 6: Check the button text is back to "Add to cart"
    btn_text = inventory_page.get_add_button_text(product_name)
    assert btn_text.lower() == "add to cart"

    # Step 7: Go to cart page and verify product is not present
    cart_page = CartPage(driver)
    cart_page.load()
    cart_page.is_loaded()
    cart_products = cart_page.get_cart_products()
    assert product_name not in cart_products
