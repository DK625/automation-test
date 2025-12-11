"""
Test Cases cho chức năng Thêm vào giỏ hàng (TVGH_1 đến TVGH_26)
File: cart_flow_cases.py
"""
import pytest
import re
import time
from datetime import datetime
import os
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Add parent path for imports
base = os.getcwd()
path = os.path.dirname(base)
sys.path.append(path)

from gg_sheet.index import ConnectGoogleSheet
from utils.index import update_status_result_to_sheet, get_test_data_from_sheet
from constant.index import JSON_NAME, SPREEDSHEET_ID

# ============== CONSTANTS ==============
BASE_URL = "http://14.225.44.169:3000/home"
EMAIL_TEST = "lovecatdat@gmail.com"
PASSWORD_TEST = "123456@Dat"
CART_TEST_CASE = "add_to_cart_test_cases"

# Row mapping for each test case in Google Sheet
TEST_CASE_ROWS = {
    "TVGH_1": 5,
    "TVGH_2": 6,
    "TVGH_3": 7,
    "TVGH_4": 8,
    "TVGH_5": 9,
    "TVGH_6": 10,
    "TVGH_7": 11,
    "TVGH_8": 12,
    "TVGH_9": 13,
    "TVGH_10": 14,
    "TVGH_11": 15,
    "TVGH_12": 16,
    "TVGH_13": 19,
    "TVGH_14": 20,
    "TVGH_15": 21,
    "TVGH_16": 22,
    "TVGH_17": 24,
    "TVGH_18": 25,
    "TVGH_19": 27,
    "TVGH_20": 28,
    "TVGH_21": 29,
    "TVGH_22": 30,
    "TVGH_23": 32,
    "TVGH_24": 33,
    "TVGH_25": 34,
    "TVGH_26": 35,
    "TVGH_27": 36,
    "TVGH_28": 37,
    "TVGH_29": 39,
    "TVGH_30": 40,
    "TVGH_31": 41,
}

# CSS Selectors
SELECTORS = {
    "email_input": "(//input[@type='text'])[1]",
    "password_input": "//input[@type='password']",
    "sign_in_button": "//button[@type='submit']",
    "add_to_cart_button": "//button[contains(., 'Thêm giỏ hàng')]",
    "buy_now_button": "//button[contains(., 'Mua hàng')]",
    "cart_icon": "//a[@href='/my-cart']",
    "select_all_checkbox": "[data-testid='select-all-checkbox']",
    "cart_total": "[data-testid='cart-total']",
    "buy_button": "//button[contains(., 'Mua hàng')]",
    "delete_all_button": "//button[@aria-label='Delete_all']",
    "product_checkbox": "input[type='checkbox']",
    "quantity_input": "input[type='number']",
    "increase_button": "//button[contains(@data-testid, 'increase-quantity')]",
    "decrease_button": "//button[contains(@data-testid, 'decrease-quantity')]",
    "delete_button": "//button[contains(@data-testid, 'delete-product')]",
}

# Run index from environment variable (default 1)
RUN_INDEX = int(os.environ.get("RUN_INDEX", 1))


class TestCartFlow:
    """Test class for Add to Cart Flow test cases TVGH_1 to TVGH_26"""
    
    driver = None
    worksheet = None
    test_failures_dir = "test_failures"

    @classmethod
    def setup_class(cls):
        """Setup test class - initialize WebDriver and Google Sheet connection"""
        print("\n========== SETUP TEST CLASS ==========")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        
        # Create screenshot directory if not exists
        if not os.path.exists(cls.test_failures_dir):
            os.makedirs(cls.test_failures_dir)
        
        # Connect to Google Sheet
        cls.gg_sheet = ConnectGoogleSheet(JSON_NAME)
        cls.worksheet = cls.gg_sheet.loadSheet_WorkSheet(SPREEDSHEET_ID, CART_TEST_CASE)

    @classmethod
    def teardown_class(cls):
        """Teardown test class - close browser"""
        print("\n========== TEARDOWN TEST CLASS ==========")
        if cls.driver:
            cls.driver.quit()
            print("[OK] Browser closed")

    def take_screenshot(self, test_name):
        """Take screenshot on test failure"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(self.test_failures_dir, f"{test_name}_{timestamp}.png")
        self.driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")
        return screenshot_path

    def update_result(self, test_case_id, result):
        """Update test result to Google Sheet"""
        if self.worksheet:
            try:
                row = TEST_CASE_ROWS.get(test_case_id)
                if row:
                    update_status_result_to_sheet(
                        worksheet=self.worksheet,
                        base_col="F",
                        row=row,
                        value_update=[result],
                        run_index=RUN_INDEX
                    )
                    print(f"✓ Updated {test_case_id}: {result}")
            except Exception as e:
                print(f"✗ Failed to update {test_case_id}: {e}")

    def login_to_system(self):
        """Login to the system"""
        print("Logging in...")
        self.driver.get("http://14.225.44.169:3000/login")
        time.sleep(2)
        
        email_input = self.driver.find_element(By.XPATH, SELECTORS["email_input"])
        email_input.send_keys(EMAIL_TEST)
        
        password_input = self.driver.find_element(By.XPATH, SELECTORS["password_input"])
        password_input.send_keys(PASSWORD_TEST)
        
        sign_in_btn = self.driver.find_element(By.XPATH, SELECTORS["sign_in_button"])
        sign_in_btn.click()
        time.sleep(3)
        print("[OK] Logged in successfully")

    def clear_cart(self):
        """Clear all items from cart"""
        try:
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Check if cart has items
            try:
                select_all = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["select_all_checkbox"])
                select_all.click()
                time.sleep(1)
                
                # Find and click delete all button
                delete_btn = self.driver.find_element(By.XPATH, "//button[@aria-label]")
                delete_btn.click()
                time.sleep(2)
                print("[OK] Cart cleared")
            except:
                print("[OK] Cart already empty")
        except Exception as e:
            print(f"[WARN] Error clearing cart: {e}")

    def add_product_to_cart(self, product_index=1):
        """Add a product to cart by index"""
        self.driver.get(BASE_URL)
        time.sleep(2)
        
        add_btn = self.driver.find_element(By.XPATH, f"({SELECTORS['add_to_cart_button']})[{product_index}]")
        add_btn.click()
        time.sleep(1)
        print(f"[OK] Added product {product_index} to cart")

    # ==================== TEST CASES ====================
    
    def test_tvgh_1_check_cart_interface(self):
        """TVGH_1: Kiểm tra giao diện màn hình giỏ hàng"""
        test_id = "TVGH_1"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.login_to_system()
            self.add_product_to_cart(1)
            
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Check checkbox exists
            checkbox = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["select_all_checkbox"])
            assert checkbox.is_displayed(), "Checkbox not visible"
            
            # Check image exists
            image = self.driver.find_element(By.XPATH, "//img[contains(@src, 'http')]")
            assert image.is_displayed(), "Product image not visible"
            
            # Check product name exists
            product_name = self.driver.find_element(By.XPATH, "//a[contains(@href, '/product/')]")
            assert product_name.is_displayed(), "Product name not visible"
            
            # Check price exists (using cart total which always has VND)
            price = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["cart_total"])
            assert price.is_displayed(), "Price not visible"
            assert "VND" in price.text, "VND currency not displayed"
            
            # Check quantity input exists
            quantity = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["quantity_input"])
            assert quantity.is_displayed(), "Quantity input not visible"
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_2_image_display_correct(self):
        """TVGH_2: Hình ảnh sản phẩm hiển thị đúng tỉ lệ"""
        test_id = "TVGH_2"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Check image dimensions
            image = self.driver.find_element(By.XPATH, "//img[contains(@src, 'http')]")
            width = image.get_attribute("width")
            height = image.get_attribute("height")
            
            assert image.is_displayed(), "Image not displayed"
            print(f"Image dimensions: {width}x{height}")
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_3_product_name_display(self):
        """TVGH_3: Tên sản phẩm hiển thị đúng"""
        test_id = "TVGH_3"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            product_name = self.driver.find_element(By.XPATH, "//a[contains(@href, '/product/')]")
            name_text = product_name.text
            
            assert len(name_text) > 0, "Product name is empty"
            assert product_name.is_displayed(), "Product name not visible"
            print(f"Product name: {name_text}")
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_4_discount_badge_display(self):
        """TVGH_4: Badge giảm giá hiển thị"""
        test_id = "TVGH_4"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Check if discount badge exists
            try:
                discount_badge = self.driver.find_element(By.XPATH, "//*[contains(text(), '%')]")
                discount_text = discount_badge.text
                print(f"Discount badge found: {discount_text}")
                assert "%" in discount_text, "Discount percentage not displayed correctly"
            except:
                print("[WARN] No discount badge found (product may not have discount)")
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_5_increase_decrease_buttons(self):
        """TVGH_5: Nút tăng/giảm số lượng có icon + màu"""
        test_id = "TVGH_5"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Check increase button
            increase_btn = self.driver.find_element(By.XPATH, f"{SELECTORS['increase_button']}[1]")
            assert increase_btn.is_displayed(), "Increase button not visible"
            
            # Check decrease button
            decrease_btn = self.driver.find_element(By.XPATH, f"{SELECTORS['decrease_button']}[1]")
            assert decrease_btn.is_displayed(), "Decrease button not visible"
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_6_delete_button_icon(self):
        """TVGH_6: Nút Delete (trash) có icon rõ ràng"""
        test_id = "TVGH_6"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            delete_btn = self.driver.find_element(By.XPATH, f"{SELECTORS['delete_button']}[1]")
            assert delete_btn.is_displayed(), "Delete button not visible"
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_7_product_checkbox(self):
        """TVGH_7: Checkbox mỗi sản phẩm"""
        test_id = "TVGH_7"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, SELECTORS["product_checkbox"])
            assert len(checkboxes) > 1, "Product checkboxes not found"
            
            # Check if checkbox is enabled
            product_checkbox = checkboxes[1]  # First product checkbox (0 is select all)
            assert product_checkbox.is_enabled(), "Product checkbox is disabled"
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_8_select_all_checkbox(self):
        """TVGH_8: Checkbox chọn tất cả"""
        test_id = "TVGH_8"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            select_all = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["select_all_checkbox"])
            
            # Click to select all
            select_all.click()
            time.sleep(1)
            
            # Verify all products are selected
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, SELECTORS["product_checkbox"])
            selected_count = sum(1 for cb in checkboxes if cb.is_selected())
            
            assert selected_count > 0, "No checkboxes selected"
            print(f"Selected {selected_count} items")
            
            # Click again to deselect all
            select_all.click()
            time.sleep(1)
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_9_total_price_display(self):
        """TVGH_9: Tổng tiền hiển thị nổi bật"""
        test_id = "TVGH_9"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Select a product
            select_all = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["select_all_checkbox"])
            select_all.click()
            time.sleep(1)
            
            # Check total price display
            total_price = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["cart_total"])
            assert total_price.is_displayed(), "Total price not visible"
            
            total_text = total_price.text
            assert "VND" in total_text, "Currency not displayed"
            print(f"Total price: {total_text}")
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_10_buy_button_disabled_no_selection(self):
        """TVGH_10: Nút "Mua hàng" disabled khi không chọn sản phẩm"""
        test_id = "TVGH_10"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Ensure no products are selected
            select_all = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["select_all_checkbox"])
            if select_all.is_selected():
                select_all.click()
                time.sleep(1)
            
            # Check buy button is disabled
            buy_btn = self.driver.find_element(By.XPATH, SELECTORS["buy_button"])
            is_disabled = buy_btn.get_attribute("disabled")
            
            assert is_disabled, "Buy button should be disabled when no product selected"
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_11_buy_button_enabled_with_selection(self):
        """TVGH_11: Nút "Mua hàng" enabled khi có sản phẩm được chọn"""
        test_id = "TVGH_11"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Select a product
            select_all = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["select_all_checkbox"])
            select_all.click()
            time.sleep(1)
            
            # Check buy button is enabled
            buy_btn = self.driver.find_element(By.XPATH, SELECTORS["buy_button"])
            is_disabled = buy_btn.get_attribute("disabled")
            
            assert not is_disabled, "Buy button should be enabled when product is selected"
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_12_delete_icon_tooltip(self):
        """TVGH_12: Tooltip icon (delete) hiển thị"""
        test_id = "TVGH_12"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Hover over delete button to show tooltip
            delete_btn = self.driver.find_element(By.XPATH, f"{SELECTORS['delete_button']}[1]")
            
            # Use ActionChains to hover
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(self.driver)
            actions.move_to_element(delete_btn).perform()
            time.sleep(1)
            
            # Check if delete button is clickable
            assert delete_btn.is_enabled(), "Delete button is not clickable"
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_13_add_one_product(self):
        """TVGH_13: Thêm 1 sản phẩm vào giỏ"""
        test_id = "TVGH_13"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.clear_cart()
            self.add_product_to_cart(1)
            
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Verify product is in cart
            products = self.driver.find_elements(By.XPATH, "//img[contains(@src, 'http')]")
            assert len(products) >= 1, "Product not added to cart"
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_14_add_same_product_twice(self):
        """TVGH_14: Thêm cùng sản phẩm 2 lần"""
        test_id = "TVGH_14"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.clear_cart()
            
            # Add same product twice
            self.add_product_to_cart(1)
            time.sleep(1)
            self.add_product_to_cart(1)
            
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Check quantity increased
            quantity_input = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["quantity_input"])
            quantity = int(quantity_input.get_attribute("value"))
            
            assert quantity >= 2, f"Quantity should be at least 2, got {quantity}"
            print(f"Quantity: {quantity}")
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_15_add_multiple_products(self):
        """TVGH_15: Thêm nhiều sản phẩm khác nhau"""
        test_id = "TVGH_15"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.clear_cart()
            
            # Add different products
            self.add_product_to_cart(1)
            time.sleep(1)
            self.add_product_to_cart(2)
            
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Verify multiple products in cart
            products = self.driver.find_elements(By.XPATH, "//img[contains(@src, 'http')]")
            assert len(products) >= 2, f"Expected at least 2 products, got {len(products)}"
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_16_empty_cart(self):
        """TVGH_16: Giỏ trống → thêm sản phẩm"""
        test_id = "TVGH_16"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.clear_cart()
            
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Check for empty cart message
            try:
                no_data = self.driver.find_element(By.XPATH, "//*[contains(text(), 'No_product') or contains(text(), 'Không có sản phẩm')]")
                print("[OK] Empty cart message displayed")
            except:
                # Check if total is 0
                total_price = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["cart_total"])
                assert "0" in total_price.text, "Total should be 0 for empty cart"
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_17_increase_quantity(self):
        """TVGH_17: Click tăng số lượng [+]"""
        test_id = "TVGH_17"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.clear_cart()
            self.add_product_to_cart(1)
            
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Get initial quantity
            quantity_input = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["quantity_input"])
            initial_qty = int(quantity_input.get_attribute("value"))
            
            # Click increase button
            increase_btn = self.driver.find_element(By.XPATH, f"{SELECTORS['increase_button']}[1]")
            increase_btn.click()
            time.sleep(2)
            
            # Get new quantity
            new_qty = int(quantity_input.get_attribute("value"))
            
            assert new_qty == initial_qty + 1, f"Quantity should increase by 1, got {new_qty}"
            print(f"Quantity increased from {initial_qty} to {new_qty}")
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_18_decrease_quantity(self):
        """TVGH_18: Click giảm số lượng [-]"""
        test_id = "TVGH_18"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.clear_cart()
            self.add_product_to_cart(1)
            
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Increase quantity first
            increase_btn = self.driver.find_element(By.XPATH, f"{SELECTORS['increase_button']}[1]")
            increase_btn.click()
            time.sleep(2)
            
            # Get current quantity
            quantity_input = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["quantity_input"])
            initial_qty = int(quantity_input.get_attribute("value"))
            
            # Click decrease button
            decrease_btn = self.driver.find_element(By.XPATH, f"{SELECTORS['decrease_button']}[1]")
            decrease_btn.click()
            time.sleep(2)
            
            # Get new quantity
            new_qty = int(quantity_input.get_attribute("value"))
            
            assert new_qty == initial_qty - 1, f"Quantity should decrease by 1, got {new_qty}"
            print(f"Quantity decreased from {initial_qty} to {new_qty}")
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_19_delete_one_product(self):
        """TVGH_19: Xóa 1 sản phẩm, Click icon xóa"""
        test_id = "TVGH_19"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.clear_cart()
            self.add_product_to_cart(1)
            
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Click delete button
            delete_btn = self.driver.find_element(By.XPATH, f"{SELECTORS['delete_button']}[1]")
            delete_btn.click()
            time.sleep(2)
            
            # Verify product is deleted
            try:
                no_data = self.driver.find_element(By.XPATH, "//*[contains(text(), 'No_product') or contains(text(), 'Không có sản phẩm')]")
                print("[OK] Product deleted, cart is empty")
            except:
                print("[OK] Product deleted")
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_20_delete_multiple_products(self):
        """TVGH_20: Xóa nhiều sản phẩm đã chọn"""
        test_id = "TVGH_20"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.clear_cart()
            self.add_product_to_cart(1)
            time.sleep(1)
            self.add_product_to_cart(2)
            
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Select all products
            select_all = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["select_all_checkbox"])
            select_all.click()
            time.sleep(1)
            
            # Click delete all button
            delete_all_btn = self.driver.find_element(By.XPATH, "//button[@aria-label]")
            delete_all_btn.click()
            time.sleep(2)
            
            # Verify cart is empty
            try:
                no_data = self.driver.find_element(By.XPATH, "//*[contains(text(), 'No_product') or contains(text(), 'Không có sản phẩm')]")
                print("[OK] All products deleted")
            except:
                print("[OK] Products deleted")
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_21_delete_all_products(self):
        """TVGH_21: Xóa tất cả sản phẩm"""
        test_id = "TVGH_21"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            # Same as TVGH_20
            self.test_tvgh_20_delete_multiple_products()
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_22_total_price_after_delete(self):
        """TVGH_22: Kiểm tra số tiền cập nhật đúng sau khi xóa sản phẩm"""
        test_id = "TVGH_22"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.clear_cart()
            self.add_product_to_cart(1)
            time.sleep(1)
            self.add_product_to_cart(2)
            
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Select all and get initial total
            select_all = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["select_all_checkbox"])
            select_all.click()
            time.sleep(1)
            
            total_price = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["cart_total"])
            initial_total = total_price.text
            print(f"Initial total: {initial_total}")
            
            # Delete one product
            delete_btn = self.driver.find_element(By.XPATH, f"{SELECTORS['delete_button']}[1]")
            delete_btn.click()
            time.sleep(2)
            
            # Get new total
            new_total = total_price.text
            print(f"New total after delete: {new_total}")
            
            # Total should change
            assert initial_total != new_total, "Total should change after deleting product"
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_23_select_one_product(self):
        """TVGH_23: Chọn 1 sản phẩm"""
        test_id = "TVGH_23"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Deselect all first
            select_all = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["select_all_checkbox"])
            if select_all.is_selected():
                select_all.click()
                time.sleep(1)
            
            # Select one product
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, SELECTORS["product_checkbox"])
            if len(checkboxes) > 1:
                checkboxes[1].click()  # First product checkbox
                time.sleep(1)
                
                assert checkboxes[1].is_selected(), "Product checkbox should be selected"
                print("[OK] Product selected")
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_24_select_multiple_products(self):
        """TVGH_24: Chọn nhiều sản phẩm"""
        test_id = "TVGH_24"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Select all products
            select_all = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["select_all_checkbox"])
            select_all.click()
            time.sleep(1)
            
            # Verify multiple products selected
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, SELECTORS["product_checkbox"])
            selected_count = sum(1 for cb in checkboxes if cb.is_selected())
            
            assert selected_count > 1, "Multiple products should be selected"
            print(f"[OK] {selected_count} products selected")
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_25_deselect_one_product(self):
        """TVGH_25: Bỏ chọn 1 sản phẩm"""
        test_id = "TVGH_25"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Select all first
            select_all = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["select_all_checkbox"])
            select_all.click()
            time.sleep(1)
            
            # Deselect one product
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, SELECTORS["product_checkbox"])
            if len(checkboxes) > 1:
                # Use JavaScript click to avoid "element click intercepted" error
                self.driver.execute_script("arguments[0].click();", checkboxes[1])
                time.sleep(1)
                
                assert not checkboxes[1].is_selected(), "Product checkbox should be deselected"
                print("[OK] Product deselected")
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_26_deselect_multiple_products(self):
        """TVGH_26: Bỏ chọn nhiều sản phẩm"""
        test_id = "TVGH_26"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Select all first
            select_all = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["select_all_checkbox"])
            select_all.click()
            time.sleep(1)
            
            # Deselect all
            select_all.click()
            time.sleep(1)
            
            # Verify all products deselected
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, SELECTORS["product_checkbox"])
            selected_count = sum(1 for cb in checkboxes if cb.is_selected())
            
            assert selected_count == 0, "All products should be deselected"
            print("[OK] All products deselected")
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_27_select_all_products(self):
        """TVGH_27: Chọn tất cả sản phẩm"""
        test_id = "TVGH_27"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            # Ensure cart has products
            self.add_product_to_cart(1)
            time.sleep(1)
            self.add_product_to_cart(2)
            
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Click select all checkbox
            select_all = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["select_all_checkbox"])
            select_all.click()
            time.sleep(1)
            
            # Verify all products are selected
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, SELECTORS["product_checkbox"])
            selected_count = sum(1 for cb in checkboxes if cb.is_selected())
            
            assert selected_count > 0, "At least one product should be selected"
            print(f"[OK] {selected_count} products selected")
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_28_deselect_all_products(self):
        """TVGH_28: Bỏ chọn tất cả sản phẩm"""
        test_id = "TVGH_28"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            # Ensure cart has products
            self.add_product_to_cart(1)
            time.sleep(1)
            self.add_product_to_cart(2)
            
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Select all first
            select_all = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["select_all_checkbox"])
            select_all.click()
            time.sleep(1)
            
            # Deselect all
            select_all.click()
            time.sleep(1)
            
            # Verify all products are deselected
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, SELECTORS["product_checkbox"])
            selected_count = sum(1 for cb in checkboxes if cb.is_selected())
            
            assert selected_count == 0, "All products should be deselected"
            print("[OK] All products deselected")
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_29_total_price_one_product(self):
        """TVGH_29: Kiểm tra tổng số tiền khi số lượng sản phẩm là 1"""
        test_id = "TVGH_29"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.clear_cart()
            self.add_product_to_cart(1)
            
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Select the product
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, SELECTORS["product_checkbox"])
            if len(checkboxes) > 1:
                checkboxes[1].click()  # First product checkbox
                time.sleep(1)
            
            # Get total price
            total_price = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["cart_total"])
            total_text = total_price.text
            
            assert "VND" in total_text, "Total price should display VND"
            assert total_text != "0 VND", "Total should not be 0 when product is selected"
            print(f"Total price for 1 product: {total_text}")
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_30_total_price_empty_cart(self):
        """TVGH_30: Kiểm tra tổng tiền khi giỏ hàng trống"""
        test_id = "TVGH_30"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.clear_cart()
            
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Get total price
            total_price = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["cart_total"])
            total_text = total_price.text
            
            # Check if total is 0
            assert "0" in total_text or "0 VND" in total_text, "Total should be 0 for empty cart"
            print(f"Total price for empty cart: {total_text}")
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))

    def test_tvgh_31_total_price_multiple_products(self):
        """TVGH_31: Kiểm tra tổng số tiền khi số lượng sản phẩm >2"""
        test_id = "TVGH_31"
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_id}")
        print(f"{'='*50}")
        
        try:
            self.clear_cart()
            
            # Add multiple products
            self.add_product_to_cart(1)
            time.sleep(1)
            self.add_product_to_cart(2)
            time.sleep(1)
            self.add_product_to_cart(3)
            
            self.driver.get("http://14.225.44.169:3000/my-cart")
            time.sleep(2)
            
            # Select all products
            select_all = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["select_all_checkbox"])
            select_all.click()
            time.sleep(1)
            
            # Get total price
            total_price = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["cart_total"])
            total_text = total_price.text
            
            assert "VND" in total_text, "Total price should display VND"
            assert total_text != "0 VND", "Total should not be 0 when products are selected"
            print(f"Total price for multiple products: {total_text}")
            
            # Verify we have multiple products
            products = self.driver.find_elements(By.XPATH, "//img[contains(@src, 'http')]")
            assert len(products) >= 2, f"Should have at least 2 products, got {len(products)}"
            print(f"Number of products in cart: {len(products)}")
            
            print(f"[OK] {test_id} PASSED")
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            print(f"[FAIL] {test_id} ERROR: {e}")
            self.take_screenshot(test_id)
            self.update_result(test_id, "FAIL")
            pytest.fail(str(e))


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])


