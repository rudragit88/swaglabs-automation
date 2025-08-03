import pytest
import time
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


def test_cart_item_count_verification(driver):
    login_page = LoginPage(driver)
    login_page.load()
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()

    inventory_page = InventoryPage(driver)
    inventory_page.is_loaded()
    
    # Choose three different products to add
    all_products = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
    added_count = 0

    for product in all_products:
        # Add product only once
        added = inventory_page.add_product_to_cart(product)
        assert added, f"Failed to add product '{product}' to cart"
        added_count += 1

        # Small wait to let UI update before checking badge count
        time.sleep(0.5)

        # Wait for cart badge count to match the number of added products
        def badge_matches(_):
            try:
                count = inventory_page.get_cart_badge_count()
                print(f"Waiting for cart badge to be {added_count}, currently: {count}")
                return count == added_count
            except StaleElementReferenceException:
                return False

        WebDriverWait(driver, 15).until(badge_matches)
        assert inventory_page.get_cart_badge_count() == added_count

    # Remove one product
    removed = inventory_page.remove_product_from_cart(all_products[1])
    assert removed, f"Failed to remove product '{all_products[1]}' from cart"
    added_count -= 1
    time.sleep(0.5)
    WebDriverWait(driver, 15).until(lambda d: inventory_page.get_cart_badge_count() == added_count)
    assert inventory_page.get_cart_badge_count() == added_count

    # Remove another product
    removed = inventory_page.remove_product_from_cart(all_products[0])
    assert removed, f"Failed to remove product '{all_products[0]}' from cart"
    added_count -= 1
    time.sleep(0.5)
    WebDriverWait(driver, 15).until(lambda d: inventory_page.get_cart_badge_count() == added_count)
    assert inventory_page.get_cart_badge_count() == added_count

    # Remove last product
    removed = inventory_page.remove_product_from_cart(all_products[2])
    assert removed, f"Failed to remove product '{all_products[2]}' from cart"
    added_count -= 1
    time.sleep(0.5)
    WebDriverWait(driver, 15).until(lambda d: inventory_page.get_cart_badge_count() == 0)
    assert inventory_page.get_cart_badge_count() == 0

    # Verify cart page is empty
    cart_page = CartPage(driver)
    cart_page.load()
    cart_page.is_loaded()
    assert cart_page.get_cart_products() == []
