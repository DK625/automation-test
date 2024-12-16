from .base_page import BasePage
from utils.locators import LoginPageLocators


class LoginPage(BasePage):
    def login(self, email, password):
        self.input_text(LoginPageLocators.EMAIL_INPUT, email)
        self.input_text(LoginPageLocators.PASSWORD_INPUT, password)
        self.click(LoginPageLocators.SUBMIT_BUTTON)
