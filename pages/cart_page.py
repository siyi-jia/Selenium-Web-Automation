from selenium.webdriver.common.by import By


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.checkout_btn = (By.ID, "checkout")
        self.continue_shopping_btn = (By.ID, "continue-shopping")

    def click_checkout(self):
        self.driver.find_element(*self.checkout_btn).click()

    def click_continue_shopping(self):
        self.driver.find_element(*self.continue_shopping_btn).click()