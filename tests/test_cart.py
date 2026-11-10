import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

@pytest.fixture
def driver_setup():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()

# ================= 模块一：登录鉴权异常流（8条） =================
@pytest.mark.parametrize("username, password, expected_error", [
    ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out"),
    ("standard_user", "wrong_password", "Username and password do not match"),
    ("", "secret_sauce", "Username is required"),
    ("standard_user", "", "Password is required"),
    ("", "", "Username is required"),
    ("problem_user", "wrong_pwd", "Username and password do not match"),
    ("performance_glitch_user", "wrong_pwd", "Username and password do not match"),
    ("error_user", "wrong_pwd", "Username and password do not match"),
])
def test_login_negative_scenarios(driver_setup, username, password, expected_error):
    login = LoginPage(driver_setup)
    login.login(username, password)
    assert expected_error in login.get_error_message()

# ================= 模块二：商品列表与排序（6条） =================
def test_sort_price_low_to_high(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    inv = InventoryPage(driver_setup)
    inv.sort_by("lohi")
    prices = inv.get_all_prices()
    assert prices == sorted(prices)

def test_sort_price_high_to_low(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    inv = InventoryPage(driver_setup)
    inv.sort_by("hilo")
    prices = inv.get_all_prices()
    assert prices == sorted(prices, reverse=True)

def test_add_single_item(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    inv = InventoryPage(driver_setup)
    inv.add_item_to_cart("sauce-labs-backpack")
    assert inv.get_cart_count() == "1"

def test_add_multiple_items(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    inv = InventoryPage(driver_setup)
    inv.add_item_to_cart("sauce-labs-backpack")
    inv.add_item_to_cart("sauce-labs-bike-light")
    assert inv.get_cart_count() == "2"

def test_remove_item_from_inventory(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    inv = InventoryPage(driver_setup)
    inv.add_item_to_cart("sauce-labs-backpack")
    inv.remove_item_from_inventory("sauce-labs-backpack")
    assert inv.get_cart_count() == "0"

def test_continue_shopping_btn(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    InventoryPage(driver_setup).go_to_cart()
    CartPage(driver_setup).click_continue_shopping()
    assert "inventory.html" in driver_setup.current_url

# ================= 模块三：结算异常与财务校验（11条） =================
@pytest.mark.parametrize("fname, lname, zipcode, error_msg", [
    ("", "", "", "Error: First Name is required"),
    ("Test", "", "", "Error: Last Name is required"),
    ("Test", "User", "", "Error: Postal Code is required"),
    ("", "User", "123", "Error: First Name is required"),
])
def test_checkout_form_validation(driver_setup, fname, lname, zipcode, error_msg):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    inv = InventoryPage(driver_setup)
    inv.add_item_to_cart("sauce-labs-backpack")
    inv.go_to_cart()
    CartPage(driver_setup).click_checkout()
    checkout = CheckoutPage(driver_setup)
    checkout.fill_info(fname, lname, zipcode)
    assert error_msg in checkout.get_error_message()

def test_cancel_checkout(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    inv = InventoryPage(driver_setup)
    inv.add_item_to_cart("sauce-labs-backpack")
    inv.go_to_cart()
    CartPage(driver_setup).click_checkout()
    CheckoutPage(driver_setup).click_cancel()
    assert "cart.html" in driver_setup.current_url

def test_remove_item_from_cart(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    inv = InventoryPage(driver_setup)
    inv.add_item_to_cart("sauce-labs-backpack")
    inv.go_to_cart()
    CartPage(driver_setup).remove_item("sauce-labs-backpack")
    assert "cart.html" in driver_setup.current_url

def test_financial_calculation_check(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    inv = InventoryPage(driver_setup)
    inv.add_item_to_cart("sauce-labs-backpack")
    inv.add_item_to_cart("sauce-labs-bike-light")
    inv.go_to_cart()
    CartPage(driver_setup).click_checkout()
    checkout = CheckoutPage(driver_setup)
    checkout.fill_info("Test", "User", "100000")
    subtotal, tax, total = checkout.get_prices_on_summary()
    assert round(subtotal + tax, 2) == total, "财务计算精度错误"

def test_e2e_successful_checkout(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    inv = InventoryPage(driver_setup)
    inv.add_item_to_cart("sauce-labs-backpack")
    inv.go_to_cart()
    CartPage(driver_setup).click_checkout()
    checkout = CheckoutPage(driver_setup)
    checkout.fill_info("Test", "User", "100000")
    checkout.click_finish()
    assert "Thank you for your order!" in checkout.get_success_message()