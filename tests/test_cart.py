import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.fixture
def driver_setup():
    driver = webdriver.Chrome()
    # 【关键修复】加入隐式等待，防止网页加载慢导致找不到元素
    driver.implicitly_wait(5)
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()


# ================= 模块一：登录异常场景测试 =================
@pytest.mark.parametrize("username, password, expected_error", [
    ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
    ("standard_user", "wrong_password", "Epic sadface: Username and password do not match any user in this service"),
    ("", "secret_sauce", "Epic sadface: Username is required"),
])
def test_login_negative_scenarios(driver_setup, username, password, expected_error):
    login_page = LoginPage(driver_setup)
    login_page.login(username, password)
    assert expected_error in login_page.get_error_message()


# ================= 模块二：商品列表与购物车操作 =================
def test_product_sorting(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    inv_page = InventoryPage(driver_setup)
    inv_page.sort_by("lohi")
    prices = inv_page.get_all_prices()
    assert prices == sorted(prices), "商品未能正确按价格升序排列"


def test_add_and_remove_items_from_cart(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    inv_page = InventoryPage(driver_setup)
    inv_page.add_item_to_cart("sauce-labs-backpack")
    inv_page.add_item_to_cart("sauce-labs-bike-light")
    assert inv_page.get_cart_count() == "2"
    inv_page.remove_item_from_cart("sauce-labs-backpack")
    assert inv_page.get_cart_count() == "1", "移除商品后购物车数量未正确减少"


def test_continue_shopping_from_cart(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    InventoryPage(driver_setup).go_to_cart()
    cart_page = CartPage(driver_setup)
    cart_page.click_continue_shopping()
    assert "inventory.html" in driver_setup.current_url, "未能返回商品列表页"


# ================= 模块三：订单结算与异常校验 =================
def test_checkout_missing_fields(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    InventoryPage(driver_setup).add_item_to_cart("sauce-labs-backpack")
    InventoryPage(driver_setup).go_to_cart()
    CartPage(driver_setup).click_checkout()
    checkout_page = CheckoutPage(driver_setup)
    checkout_page.fill_info("", "", "")
    assert "Error: First Name is required" in checkout_page.get_error_message()


def test_cancel_checkout_process(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    InventoryPage(driver_setup).add_item_to_cart("sauce-labs-backpack")
    InventoryPage(driver_setup).go_to_cart()
    CartPage(driver_setup).click_checkout()
    checkout_page = CheckoutPage(driver_setup)
    checkout_page.click_cancel()
    assert "cart.html" in driver_setup.current_url, "取消结算未能返回购物车"


def test_financial_calculation_check(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    InventoryPage(driver_setup).add_item_to_cart("sauce-labs-backpack")
    InventoryPage(driver_setup).go_to_cart()
    CartPage(driver_setup).click_checkout()

    checkout_page = CheckoutPage(driver_setup)
    checkout_page.fill_info("Test", "User", "100000")

    subtotal, tax, total = checkout_page.get_prices_on_summary()
    assert round(subtotal + tax, 2) == total, "订单总金额计算错误"


# ================= 模块四：正向端到端全流程 =================
def test_e2e_successful_checkout(driver_setup):
    LoginPage(driver_setup).login("standard_user", "secret_sauce")
    InventoryPage(driver_setup).add_item_to_cart("sauce-labs-backpack")
    InventoryPage(driver_setup).go_to_cart()
    CartPage(driver_setup).click_checkout()

    checkout_page = CheckoutPage(driver_setup)
    checkout_page.fill_info("Test", "User", "100000")
    checkout_page.click_finish()
    assert "Thank you for your order!" in checkout_page.get_success_message()