from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.sort_dropdown = (By.CLASS_NAME, "product_sort_container")
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
        self.cart_icon = (By.CLASS_NAME, "shopping_cart_link")
        self.item_prices = (By.CLASS_NAME, "inventory_item_price")

    def sort_by(self, value):
        # 传入 'lohi' (价格低到高), 'hilo' (价格高到低), 'az', 'za'
        Select(self.driver.find_element(*self.sort_dropdown)).select_by_value(value)

    def get_all_prices(self):
        # 获取页面上所有商品的价格（去掉$符号，转为浮点数）
        elements = self.driver.find_elements(*self.item_prices)
        return [float(el.text.replace("$", "")) for el in elements]

    def add_item_to_cart(self, item_name):
        # 根据商品名字动态点击对应的添加按钮
        item_id = f"add-to-cart-{item_name}"
        self.driver.find_element(By.ID, item_id).click()

    def remove_item_from_cart(self, item_name):
        item_id = f"remove-{item_name}"
        self.driver.find_element(By.ID, item_id).click()

    def get_cart_count(self):
        try:
            return self.driver.find_element(*self.cart_badge).text
        except:
            return "0" # 如果购物车图标上没有数字，说明是0

    def go_to_cart(self):
        self.driver.find_element(*self.cart_icon).click()