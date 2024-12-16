from .base_page import BasePage
from utils.locators import CartPageLocators


class CartPage(BasePage):
    def get_quantity(self):
        return int(self.find_element(CartPageLocators.QUANTITY_INPUT).get_attribute('value'))

    def increase_quantity(self, times=1):
        for _ in range(times):
            self.click(CartPageLocators.INCREASE_BUTTON)

    def decrease_quantity(self, times=1):
        for _ in range(times):
            self.click(CartPageLocators.DECREASE_BUTTON)

    def delete_product(self):
        self.click(CartPageLocators.DELETE_BUTTON)

    def get_total_amount(self):
        total_text = self.find_element(CartPageLocators.TOTAL_AMOUNT).text
        return int(total_text.replace('.', '').replace(' VND', ''))
