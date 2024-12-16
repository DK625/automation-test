from .base_page import BasePage
from utils.locators import HomePageLocators


class HomePage(BasePage):
    def open_cart(self):
        self.click(HomePageLocators.CART_ICON)

    def close_cart(self):
        self.click(HomePageLocators.BACKDROP)

    def select_phones_tab(self):
        self.click(HomePageLocators.PHONE_TAB)

    def add_product_to_cart(self):
        self.click(HomePageLocators.ADD_TO_CART_BUTTON)

    def get_cart_count(self):
        return int(self.find_element(HomePageLocators.CART_BADGE).text)
