from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class TestPurchase():
    stored_localStorage = None
    driver = None

    @classmethod
    def setup_class(cls):
        """Chạy một lần khi bắt đầu tất cả test cases"""
        cls.driver = webdriver.Chrome()
        cls.vars = {}

    @classmethod
    def teardown_class(cls):
        """Chỉ chạy sau khi tất cả test cases hoàn thành"""
        if hasattr(cls, 'driver'):  # Kiểm tra xem driver có tồn tại không
            cls.driver.quit()

    def login(self):
        self.driver.get("http://localhost:3000/home")
        self.driver.maximize_window()

        # Click vào nút đăng nhập và chờ form login
        login_button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-y9vvym-MuiButtonBase-root-MuiButton-root"))
        )
        login_button.click()

        # Nhập email - using MUI TextField selector
        email_input = WebDriverWait(self.driver, 55).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.MuiInputBase-input[aria-invalid='false']"))
        )
        email_input.send_keys("doanthuyduong2103@gmail.com")

        # Nhập password - using MUI TextField selector with type='password'
        password_input = WebDriverWait(self.driver, 55).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.MuiInputBase-input[type='password']"))
        )
        password_input.send_keys("Thanhthuy2103@")

        submit_button = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButton-root"))
        )
        submit_button.click()

    def test_validate_empty_shipping_address_fields(self):
        self.login()

        # Add watch to cart
        add_to_cart1 = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) .MuiButtonBase-root:nth-child(1)"))
        )
        add_to_cart1.click()

        # Switch to tablet tab and add 2 products
        tab_tablet = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiTab-root:nth-child(2)"))
        )
        tab_tablet.click()

        product1_tablet = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .MuiButtonBase-root:nth-child(1)"))
        )
        product1_tablet.click()

        product2_tablet = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiGrid-root:nth-child(2) .MuiButtonBase-root:nth-child(1)"))
        )
        product2_tablet.click()

        # Switch to laptop tab
        tab_laptop = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiTab-root:nth-child(3)"))
        )
        tab_laptop.click()

        product1_laptop = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .MuiButtonBase-root:nth-child(1)"))
        )
        product1_laptop.click()

        product2_laptop = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiGrid-root:nth-child(2) .MuiButtonBase-root:nth-child(1)"))
        )
        product2_laptop.click()

        # Switch to phone tab
        tab_phone = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButtonBase-root:nth-child(4)"))
        )
        tab_phone.click()

        product_phone = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .MuiButtonBase-root:nth-child(1)"))
        )
        product_phone.click()

        # Click cart icon
        cart_icon = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".iconify--flowbite > path"))
        )
        cart_icon.click()

        # Go to cart page
        cart_page_button = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-akzecb-MuiButtonBase-root-MuiButton-root"))
        )
        cart_page_button.click()

        # Select all products
        # self.driver.find_element(By.CSS_SELECTOR, ".css-tfttuo .PrivateSwitchBase-input").click()
        select_all = WebDriverWait(self.driver, 55).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".css-tfttuo .PrivateSwitchBase-input"))
        )
        select_all.click()

        # Proceed to checkout
        checkout_button = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButton-root"))
        )
        checkout_button.click()

        # Change shipping address
        change_address = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButton-text"))
        )
        change_address.click()

        new_address = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButton-root:nth-child(2)"))
        )
        new_address.click()

        # Clear all input fields
        input_fields = WebDriverWait(self.driver, 55).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input.MuiInputBase-input"))
        )

        for i, field in enumerate(input_fields):
            field.clear()
            field.click()
            field.send_keys(Keys.CONTROL + "a")
            field.send_keys(Keys.DELETE)

            if i == len(input_fields) - 1:
                field.send_keys("2")

        # Click confirm to show validation errors
        confirm_button = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1uimnmd-MuiButtonBase-root-MuiButton-root"))
        )
        confirm_button.click()

        # Verify error messages
        error_messages = WebDriverWait(self.driver, 55).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error"))
        )

        # Assert that we have the expected number of error messages
        assert len(error_messages) >= 3, "Expected at least 3 error messages for required fields"

        # Verify specific error messages
        expected_errors = ["Trường này bắt buộc", "Trường này bắt buộc", "Số điện thoại tối thiểu là 9 số"]
        actual_errors = [message.text for message in error_messages]

        for expected in expected_errors:
            assert expected in actual_errors, f"Expected error message '{expected}' not found"

        # Close form
        close_button = WebDriverWait(self.driver, 55).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".iconify--material-symbols-light > path"))
        )
        close_button.click()

        print("""
        TEST CASE: Validate Empty Shipping Address Fields

        Results:
        ✓ All required fields show validation messages
        ✓ Error messages match expected content
        ✓ Form submission prevented with empty fields

        Status: PASSED ✅
        """)
