import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

@pytest.fixture
def driver():
    service = Service()
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_add_product_to_cart(driver):
    # Login first (reuse LoginPage)
    login_page = LoginPage(driver)
    login_page.load()
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()

    # Wait for inventory page to load
    inventory_page = InventoryPage(driver)
    inventory_page.is_loaded()

    product_name = "Sauce Labs Backpack"

    # Initially cart should be empty
    assert inventory_page.get_cart_badge_count() == 0

    # Button text should be "Add to cart"
    btn_text_before = inventory_page.get_add_button_text(product_name)
    assert btn_text_before.lower() == "add to cart"

    # Add product to cart
    added = inventory_page.add_product_to_cart(product_name)
    assert added is True

    # Wait for cart badge to update
    WebDriverWait(driver, 10).until(
        lambda d: inventory_page.get_cart_badge_count() == 1
    )
    assert inventory_page.get_cart_badge_count() == 1

    # Button text changes to "Remove"
    btn_text_after = inventory_page.get_add_button_text(product_name)
    assert btn_text_after.lower() == "remove"

    # Go to Cart page and verify product is listed
    driver.get("https://www.saucedemo.com/cart.html")
    cart_page = CartPage(driver)
    cart_page.is_loaded()
    cart_products = cart_page.get_cart_products()
    assert product_name in cart_products
