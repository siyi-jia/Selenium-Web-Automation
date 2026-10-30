from selenium.webdriver.common.by import By

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.first_name = (By.ID, "first-name")
        self.last_name = (By.ID, "last-name")
        self.zip_code = (By.ID, "postal-code")
        self.continue_btn = (By.ID, "continue")
        self.cancel_btn = (By.ID, "cancel")
        self.finish_btn = (By.ID, "finish")
        self.error_msg = (By.CSS_SELECTOR, "h3[data-test='error']")
        self.success_header = (By.CLASS_NAME, "complete-header")
        self.subtotal_label = (By.CLASS_NAME, "summary_subtotal_label")
        self.tax_label = (By.CLASS_NAME, "summary_tax_label")
        self.total_label = (By.CLASS_NAME, "summary_total_label")

    def fill_info(self, fname, lname, zipcode):
        if fname: self.driver.find_element(*self.first_name).send_keys(fname)
        if lname: self.driver.find_element(*self.last_name).send_keys(lname)
        if zipcode: self.driver.find_element(*self.zip_code).send_keys(zipcode)
        self.driver.find_element(*self.continue_btn).click()

    def click_finish(self):
        self.driver.find_element(*self.finish_btn).click()

    def click_cancel(self):
        self.driver.find_element(*self.cancel_btn).click()

    def get_error_message(self):
        return self.driver.find_element(*self.error_msg).text

    def get_success_message(self):
        return self.driver.find_element(*self.success_header).text

    def get_prices_on_summary(self):
        # 获取结账页面的小计、税费和总计
        subtotal = float(self.driver.find_element(*self.subtotal_label).text.split("$")[1])
        tax = float(self.driver.find_element(*self.tax_label).text.split("$")[1])
        total = float(self.driver.find_element(*self.total_label).text.split("$")[1])
        return subtotal, tax, total