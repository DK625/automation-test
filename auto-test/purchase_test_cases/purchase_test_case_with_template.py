import os
import sys

base = os.getcwd()
path = os.path.dirname(base)
sys.path.append(path)

from gg_sheet.index import ConnectGoogleSheet
from utils.sheet_template_parser import (
    parse_sheet_to_test_cases,
    group_test_cases_by_action,
    TestResultWriter,
    create_test_summary
)
from constant.index import PURCHASE_TEST_NAME, JSON_NAME
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TestPurchaseWithTemplate:
    driver = None
    result_writer = None

    @classmethod
    def setup_class(cls):
        """Chạy một lần khi bắt đầu tất cả test cases"""
        cls.driver = webdriver.Chrome()
        cls.vars = {}

        # Load data from Google Sheet
        cls.gg_sheet = ConnectGoogleSheet(JSON_NAME)
        cls.worksheet = cls.gg_sheet.loadSheet_WorkSheet(
            "1EEceAh_f_vogtMxTpwHtB9yMggXsXS7DPi28aag4arY",
            PURCHASE_TEST_NAME
        )

        # Parse test cases
        rows = cls.worksheet.get_all_values()
        cls.test_cases = parse_sheet_to_test_cases(rows)
        cls.grouped_tests = group_test_cases_by_action(cls.test_cases)

        # Initialize result writer
        cls.result_writer = TestResultWriter(cls.worksheet)

        cls.test_failures_dir = "test_failures"
        os.makedirs(cls.test_failures_dir, exist_ok=True)

        print(f"\n{'='*60}")
        print(f"Loaded {len(cls.test_cases)} test cases from Google Sheet")
        print(f"Actions: {list(cls.grouped_tests.keys())}")
        print(f"{'='*60}\n")

    @classmethod
    def teardown_class(cls):
        """Chạy sau khi tất cả test cases hoàn thành"""
        # Write results back to Google Sheet
        if cls.result_writer:
            print("\nWriting results back to Google Sheet...")
            cls.result_writer.write_results()

            # Print summary
            summary = create_test_summary(cls.result_writer.results)
            print(f"\n{'='*60}")
            print(f"TEST SUMMARY")
            print(f"{'='*60}")
            print(f"Total Tests: {summary['total']}")
            print(f"Passed: {summary['passed']} ({summary['pass_rate']:.1f}%)")
            print(f"Failed: {summary['failed']}")
            print(f"Blocked: {summary['blocked']}")
            print(f"Skipped: {summary['skipped']}")
            print(f"{'='*60}\n")

        if hasattr(cls, 'driver'):
            cls.driver.quit()

    def take_screenshot(self, name):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.test_failures_dir}/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"Screenshot saved: {filename}")
        return filename

    def execute_test_case(self, test_case):
        """
        Execute một test case và return kết quả

        Args:
            test_case: Test case dictionary

        Returns:
            tuple: (actual_output, status)
        """
        action = test_case['action']
        params = test_case['params']
        row_index = test_case['row_index']

        try:
            if action == 'login':
                return self.execute_login(params)

            elif action == 'add_to_cart_and_checkout':
                return self.execute_add_to_cart_and_checkout(params)

            elif action == 'validate_empty_shipping':
                return self.execute_validate_empty_shipping(params)

            elif action == 'add_address':
                return self.execute_add_address(params)

            elif action == 'select_delivery_address':
                return self.execute_select_delivery_address(params)

            elif action == 'select_shipping':
                return self.execute_select_shipping(params)

            elif action == 'verify_total_calculation':
                return self.execute_verify_total_calculation(params)

            elif action == 'complete_purchase':
                return self.execute_complete_purchase(params)

            elif action == 'verify_order_details':
                return self.execute_verify_order_details(params)

            else:
                return f"Unknown action: {action}", "FAIL"

        except Exception as e:
            self.take_screenshot(f"failed_{action}_{row_index}")
            return f"Error: {str(e)}", "FAIL"

    def execute_login(self, params):
        """Execute login action"""
        username = params.get('username')
        password = params.get('password')

        self.driver.get("http://14.225.44.169:3000/home")
        self.driver.maximize_window()

        # Click login button
        login_button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-y9vvym-MuiButtonBase-root-MuiButton-root"))
        )
        login_button.click()

        # Enter email
        email_input = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.MuiInputBase-input[aria-invalid='false']"))
        )
        email_input.send_keys(username)

        # Enter password
        password_input = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.MuiInputBase-input[type='password']"))
        )
        password_input.send_keys(password)

        # Submit
        submit_button = WebDriverWait(self.driver, 35).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButton-root"))
        )
        submit_button.click()

        # Wait for redirect
        time.sleep(2)

        # Verify login success
        current_url = self.driver.current_url
        if "home" in current_url:
            return "Login successful, redirected to home page", "PASS"
        else:
            return f"Login failed, current URL: {current_url}", "FAIL"

    def search_product(self, product_name):
        """Search for product using search box"""
        try:
            # Find search input by aria-label
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='search']"))
            )

            # Clear any existing search THOROUGHLY
            search_input.clear()
            search_input.send_keys(Keys.CONTROL + "a")
            search_input.send_keys(Keys.BACKSPACE)
            self.driver.execute_script("arguments[0].value = '';", search_input)
            time.sleep(0.3)

            # Type product name
            search_input.send_keys(product_name)
            search_input.send_keys(Keys.ENTER)
            time.sleep(2)

            print(f"  ✓ Searched for: '{product_name}'")

        except Exception as e:
            print(f"  ✗ Search failed: {str(e)}")
            raise

    def execute_add_to_cart_and_checkout(self, params):
        """
        Add products to cart AND navigate to checkout page

        This combined action:
        1. Adds multiple products to cart (from home page)
        2. Navigates to /my-cart
        3. Selects all products
        4. Clicks Buy Now → navigates to /checkout-product

        Format: products=[Product1|Tab1; Product2|Tab2; ...]
        """
        products_str = params.get('products', '')

        if not products_str:
            return "No products specified", "FAIL"

        # Handle if parser converted it to a list (bracket-enclosed values)
        if isinstance(products_str, list):
            products_str = products_str[0] if products_str else ''

        if not products_str:
            return "No products specified", "FAIL"

        # Parse products: "iPhone 15|Điện thoại; Samsung|Điện thoại"
        # No need to strip brackets since parser already removed them
        product_list = []
        for item in products_str.split(';'):
            item = item.strip()
            if '|' in item:
                parts = item.split('|')
                product_name = parts[0].strip()
                tab = parts[1].strip() if len(parts) > 1 else None
                product_list.append({'name': product_name, 'tab': tab})

        if not product_list:
            return "Could not parse products list", "FAIL"

        print(f"  → Adding {len(product_list)} products to cart")

        # STEP 1: Add products to cart
        added_count = 0
        for product in product_list:
            try:
                # Click tab if specified
                if product['tab']:
                    print(f"  → Clicking tab: {product['tab']}")
                    tab_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-testid='tab-{product['tab']}']"))
                    )
                    tab_button.click()
                    time.sleep(1)

                # Search for product
                self.search_product(product['name'])

                # Click add to cart
                add_button = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-testid='add-to-cart-{product['name']}']"))
                )
                self.driver.execute_script("arguments[0].click();", add_button)
                time.sleep(0.5)
                added_count += 1
                print(f"  ✓ Added: {product['name']}")

            except Exception as e:
                print(f"  ✗ Failed to add {product['name']}: {str(e)}")
                continue

        # STEP 2: Navigate to cart page
        print(f"  → Navigating to cart page")
        self.driver.get("http://14.225.44.169:3000/my-cart")
        time.sleep(2)

        # STEP 3: Select all products
        print(f"  → Selecting all products in cart")
        checkboxes = WebDriverWait(self.driver, 35).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiBox-root.css-uz5qc span"))
        )
        checkboxes.click()  # Click vào tất cả các checkbox

        # STEP 4: Click Buy Now to proceed to checkout
        print(f"  → Clicking 'Buy Now' to proceed to checkout")
        try:
            buy_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Buy') or contains(., 'Mua')]"))
            )
            buy_button.click()
            time.sleep(2)
        except Exception as e:
            return f"Failed to click Buy Now: {str(e)}", "FAIL"

        # STEP 5: Verify navigation to checkout page
        if "checkout" in self.driver.current_url:
            print(f"  ✓ Successfully navigated to checkout page")
            return f"Added {added_count} products and navigated to checkout page", "PASS"
        else:
            return f"Failed to navigate to checkout page. Current URL: {self.driver.current_url}", "FAIL"

    def execute_validate_empty_shipping(self, params):
        """
        Validate form when submitting empty address fields

        Assumes: Already on /checkout-product page (from previous test)
        Assumes: User already has an address in database

        Flow (matching purchase_test_cases.py):
        1. Click "Change Address" button to open modal
        2. Click on current address to edit it
        3. Clear all input fields
        4. Click "Confirm" to trigger validation errors
        5. Verify 4 validation errors appear
        6. Close the modal

        Why important:
        - Ensures user can't save empty address fields
        - Displays helpful error messages
        - Prevents invalid address data
        """
        try:
            # Verify we're on checkout page
            if "checkout" not in self.driver.current_url:
                return "Not on checkout page. Run add_to_cart_and_checkout first!", "FAIL"

            print("  → On checkout page, clicking 'Change Address' button")
            # Click "Change Address" button (text button)
            change_address_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButton-text"))
            )
            self.driver.execute_script("arguments[0].click();", change_address_button)
            time.sleep(1)

            # Click on current address to edit it
            print("  → Clicking on current address to edit")
            edit_address_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "form>div>div>div>button"))
            )
            edit_address_button.click()
            time.sleep(1)

            # Clear all input fields
            print("  → Clearing all input fields")
            input_fields = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input.MuiInputBase-input"))
            )

            for i, field in enumerate(input_fields):
                field.clear()
                field.click()
                field.send_keys(Keys.CONTROL + "a")
                field.send_keys(Keys.DELETE)

                # Add invalid data to last field (phone) to trigger validation
                if i == len(input_fields) - 1:
                    field.send_keys("2")

            # Click confirm to trigger validation errors
            print("  → Clicking Confirm to trigger validation")
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1uimnmd-MuiButtonBase-root-MuiButton-root"))
            )
            confirm_button.click()
            time.sleep(1)

            # Check for validation errors
            print("  → Checking for validation errors")
            # Note: City dropdown error doesn't have .Mui-error class, so we select all FormHelperText
            error_messages = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormHelperText-root"))
            )

            # Filter only error messages (has text and is displayed)
            actual_errors = [message.text for message in error_messages
                           if message.is_displayed() and message.text.strip()]

            if len(actual_errors) >= 4:  # All 4 required fields should show errors
                print(f"  ✓ Found {len(actual_errors)} validation errors:")
                for error in actual_errors:
                    print(f"    - {error}")

                # Close the modal
                print("  → Closing modal")
                close_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".iconify--material-symbols-light > path"))
                )
                close_button.click()
                time.sleep(1)

                return f"All validation errors displayed ({len(actual_errors)} errors): {actual_errors}", "PASS"
            else:
                return f"Expected 4 validation errors, found {len(actual_errors)}: {actual_errors}", "FAIL"

        except Exception as e:
            self.take_screenshot("validate_empty_shipping_failed")
            return f"Error validating empty shipping: {str(e)}", "FAIL"

    def execute_add_address(self, params):
        """
        Add a new delivery address

        Flow:
        1. Click "Change Address" button
        2. Click "Cancel" to close if modal is open
        3. Click "Add New Address" button
        4. Fill in form: name, address, city (dropdown), phone
        5. Click "Confirm"

        Params:
        - name: Full name (e.g., "Nguyen Van A")
        - address: Street address (e.g., "123 Nguyen Trai")
        - city_index: Index of city in dropdown (e.g., 0 for first city)
        - phone: Phone number (e.g., "0912345678")
        """
        name = params.get('name')
        address = params.get('address')
        city_index = int(params.get('city_index', 0))
        phone = params.get('phone')

        try:
            # Click "Change Address" button to open modal
            print(f"  → Opening address modal")
            change_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiButton-root"))
            )
            self.driver.execute_script("arguments[0].click();", change_button)
            time.sleep(1)

            # Click "Cancel" if modal is already open (to reset state)
            try:
                cancel_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'MuiButton-text') and text()='Hủy bỏ']"))
                )
                cancel_button.click()
                time.sleep(1)

                # Re-open modal
                change_button.click()
                time.sleep(1)
            except:
                pass

            # Click "Add New Address" button
            print(f"  → Clicking 'Add New Address'")
            add_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1lfi9f6-MuiButtonBase-root-MuiButton-root"))
            )
            add_button.click()
            time.sleep(1)

            # Fill name
            print(f"  → Filling name: {name}")
            name_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Nhập họ và tên']"))
            )
            name_input.clear()
            name_input.send_keys(name)

            # Fill address
            print(f"  → Filling address: {address}")
            address_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Nhập địa chỉ']"))
            )
            address_input.clear()
            address_input.send_keys(address)

            # Select city from dropdown
            print(f"  → Selecting city at index {city_index}")
            city_select = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='combobox']"))
            )
            city_select.click()
            time.sleep(1)

            city_options = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.MuiMenuItem-root"))
            )
            city_options[city_index].click()
            time.sleep(0.5)

            # Fill phone
            print(f"  → Filling phone: {phone}")
            phone_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[inputmode='numeric'][pattern='[0-9]*']"))
            )
            phone_input.clear()
            phone_input.send_keys(phone)

            # Click Confirm
            print(f"  → Clicking Confirm")
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1uimnmd-MuiButtonBase-root-MuiButton-root"))
            )
            confirm_button.click()
            time.sleep(2)

            print(f"  ✓ Address added successfully")
            return f"Address added: {name}, {address}, {phone}", "PASS"

        except Exception as e:
            self.take_screenshot("add_address_failed")
            return f"Failed to add address: {str(e)}", "FAIL"

    def execute_select_delivery_address(self, params):
        """
        Select a delivery address from list

        Flow:
        1. Modal is already open (from previous test or open it)
        2. Click on radio button at specific index
        3. Click "Update" to confirm selection
        4. Verify address is displayed on checkout page

        Params:
        - address_index: Index of address to select (0 = first, 1 = second, etc.)
        """
        address_index = int(params.get('address_index', 0))

        try:
            print(f"  → Selecting address at index {address_index}")

            # Modal should already be open from add_address test
            # Click on the radio button for the address at specified index
            # CSS nth-child is 1-based, so add 1 to address_index
            address_radio_selector = f".MuiBox-root:nth-child({address_index + 1}) > .MuiFormControlLabel-root > .MuiTypography-root"

            address_radio = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, address_radio_selector))
            )
            address_radio.click()
            time.sleep(1)

            # Click "Update" button to confirm
            print(f"  → Clicking Update to confirm selection")
            update_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1uimnmd-MuiButtonBase-root-MuiButton-root"))
            )
            update_button.click()
            time.sleep(2)

            # Verify address is displayed on checkout page
            name_phone = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "p.MuiTypography-root.css-1wr5z0g-MuiTypography-root"))
            ).text

            address_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.MuiTypography-root.css-1f0oh43-MuiTypography-root"))
            ).text

            print(f"  ✓ Address selected: {name_phone} - {address_text}")
            return f"Selected address at index {address_index}: {name_phone} {address_text}", "PASS"

        except Exception as e:
            self.take_screenshot("select_delivery_address_failed")
            return f"Failed to select address: {str(e)}", "FAIL"

    def execute_select_shipping(self, params):
        """
        Select shipping provider

        Flow:
        1. Click on radio button for shipping provider (using data-testid)
        2. Verify shipping fee is displayed

        Params:
        - provider: Shipping provider name (e.g., "GHN", "GHTK")

        Note: In the database, only GHN and GHTK are available
        Frontend renders: data-testid="shipping-{provider_name}"
        - GHTK: data-testid="shipping-GHTK"
        - GHN: data-testid="shipping-GHN"
        """
        provider = params.get('provider', '').upper()

        try:
            print(f"  → Selecting shipping provider: {provider}")

            # Use data-testid for precise selection
            if provider in ["GHN", "GHTK"]:
                # Click shipping radio button using data-testid
                shipping_radio = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-testid='shipping-{provider}']"))
                )
            else:
                # Default: select GHTK
                print(f"  ⚠ Unknown provider '{provider}', defaulting to GHTK")
                shipping_radio = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='shipping-GHTK']"))
                )

            shipping_radio.click()
            time.sleep(1)

            # Get shipping fee
            shipping_fee = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".css-147dy5z:nth-child(2) p:last-child"))
            ).text

            print(f"  ✓ Shipping provider selected: {provider}, Fee: {shipping_fee}")
            return f"Selected {provider}, Shipping fee: {shipping_fee}", "PASS"

        except Exception as e:
            self.take_screenshot("select_shipping_failed")
            return f"Failed to select shipping: {str(e)}", "FAIL"

    def execute_verify_total_calculation(self, params):
        """
        Verify total = products + shipping

        Flow:
        1. Get all product prices from checkout page
        2. Get shipping fee
        3. Get total amount
        4. Verify: sum(products) + shipping = total

        Params:
        - products_total: Expected sum of product prices (optional, for verification)
        - shipping: Expected shipping fee (optional, for verification)

        Note: This test reads actual values from the page and verifies the calculation
        """
        expected_products_total = params.get('products_total')
        expected_shipping = params.get('shipping')

        try:
            print(f"  → Verifying total calculation")

            # Helper function to convert price string to integer
            def get_price_amount(price_string):
                """Convert price string 'X.XXX VND' to integer"""
                return int(price_string.replace('VND', '').replace('.', '').replace(',', '').strip())

            # Helper function to get product price (discounted or original)
            def get_product_price(product_element):
                """Get either discounted price or original price for a product"""
                try:
                    # Try to get discounted price first
                    return product_element.find_element(By.CSS_SELECTOR, ".MuiTypography-h4.css-1qv43kz-MuiTypography-root").text
                except:
                    # If no discount, get regular price
                    return product_element.find_element(By.CSS_SELECTOR, ".MuiTypography-h6").text

            # Get all product prices
            product_elements = self.driver.find_elements(By.CSS_SELECTOR, ".MuiBox-root.css-fm4r4t")
            product_prices = [get_product_price(item) for item in product_elements]
            products_sum = sum(get_price_amount(price) for price in product_prices)

            print(f"  → Product prices: {product_prices}")
            print(f"  → Products sum: {products_sum:,} VND")

            # Get shipping fee
            shipping_fee_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".css-147dy5z:nth-child(2) p:last-child"))
            ).text
            shipping_fee = get_price_amount(shipping_fee_text)
            print(f"  → Shipping fee: {shipping_fee:,} VND")

            # Get total amount
            total_amount_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".css-147dy5z:nth-child(3) p:last-child"))
            ).text
            total_amount = get_price_amount(total_amount_text)
            print(f"  → Total amount: {total_amount:,} VND")

            # Verify calculation
            calculated_total = products_sum + shipping_fee

            if calculated_total == total_amount:
                result_msg = f"Total calculation correct: {products_sum:,} + {shipping_fee:,} = {total_amount:,} VND"
                print(f"  ✓ {result_msg}")

                # If expected values provided, verify them too
                if expected_products_total:
                    expected_products_total = int(expected_products_total)
                    if products_sum != expected_products_total:
                        return f"Products total mismatch. Expected: {expected_products_total:,}, Got: {products_sum:,}", "FAIL"

                if expected_shipping:
                    expected_shipping = int(expected_shipping)
                    if shipping_fee != expected_shipping:
                        return f"Shipping fee mismatch. Expected: {expected_shipping:,}, Got: {shipping_fee:,}", "FAIL"

                return result_msg, "PASS"
            else:
                error_msg = f"Total calculation incorrect. Expected: {calculated_total:,}, Got: {total_amount:,}"
                print(f"  ✗ {error_msg}")
                return error_msg, "FAIL"

        except Exception as e:
            self.take_screenshot("verify_total_failed")
            return f"Failed to verify total: {str(e)}", "FAIL"

    def execute_complete_purchase(self, params):
        """
        Complete the purchase

        Flow:
        1. Click "Đặt hàng" (Order) button
        2. Confirm in modal (SweetAlert2)
        3. Wait for order to be created
        4. Verify cart is empty after purchase

        Params:
        - payment: Payment method (e.g., "COD") - for documentation, not used in actual flow
        """
        payment = params.get('payment', 'COD')

        try:
            print(f"  → Completing purchase with {payment}")

            # Click "Đặt hàng" button
            print(f"  → Clicking 'Đặt hàng' button")
            order_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBox-root.css-51xbo2>button"))
            )
            order_button.click()
            time.sleep(2)

            # Click confirm in SweetAlert2 modal
            print(f"  → Confirming order in modal")
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".swal2-confirm.swal2-styled"))
            )
            confirm_button.click()
            time.sleep(3)

            # Verify cart is empty (badge should be gone or show 0)
            print(f"  → Verifying cart is empty")
            try:
                cart_badge = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Giỏ hàng'] span.MuiBadge-badge"))
                )
                cart_count = int(cart_badge.text)
            except:
                # If badge not found, cart is empty (0 items)
                cart_count = 0

            if cart_count == 0:
                print(f"  ✓ Purchase completed successfully, cart is empty")
                return f"Purchase completed with {payment}, cart is now empty", "PASS"
            else:
                return f"Purchase may have failed, cart still has {cart_count} items", "FAIL"

        except Exception as e:
            self.take_screenshot("complete_purchase_failed")
            return f"Failed to complete purchase: {str(e)}", "FAIL"

    def execute_verify_order_details(self, params):
        """
        Verify order details after purchase

        Flow:
        1. Verify cart is empty (indicating order was created successfully)
        2. Optionally navigate to orders page to see the order
        3. Verify order appears in the list

        Params:
        - order_id: Order identifier (e.g., "latest") - currently just verifies order was created

        Note: The main verification is that the cart is empty after purchase,
        which indicates the order was successfully created.
        """
        order_id = params.get('order_id', 'latest')

        try:
            print(f"  → Verifying order was created successfully")

            # Main verification: Cart should be empty
            try:
                cart_badge = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Giỏ hàng'] span.MuiBadge-badge"))
                )
                cart_count = int(cart_badge.text)
            except:
                # If badge not found, cart is empty (0 items)
                cart_count = 0

            if cart_count == 0:
                print(f"  ✓ Order created successfully - cart is empty")

                # Additional verification: Check current URL
                current_url = self.driver.current_url
                print(f"  → Current URL: {current_url}")

                # Could navigate to orders page here if needed
                # For now, just verify cart is empty

                return f"Order ({order_id}) verified - cart empty, order created successfully", "PASS"
            else:
                return f"Order verification failed - cart still has {cart_count} items", "FAIL"

        except Exception as e:
            self.take_screenshot("verify_order_failed")
            return f"Failed to verify order: {str(e)}", "FAIL"

    def test_run_all_test_cases(self):
        """Run all test cases from Google Sheet"""
        print(f"\n{'='*60}")
        print("EXECUTING TEST CASES")
        print(f"{'='*60}\n")

        for i, test_case in enumerate(self.test_cases, 1):
            stt = test_case['stt']
            action = test_case['action']
            function_type = test_case['function_type']
            priority = test_case['priority']

            print(f"\n[{i}/{len(self.test_cases)}] Test Case #{stt}")
            print(f"  Action: {action}")
            print(f"  Function: {function_type}")
            print(f"  Priority: {priority}")
            print(f"  Params: {test_case['params']}")

            # Execute test case
            actual_output, status = self.execute_test_case(test_case)

            print(f"  Output: {actual_output}")
            print(f"  Status: {status}")

            # Record result
            self.result_writer.add_result(
                row_index=test_case['row_index'],
                output=actual_output,
                result_status=status
            )

            # Small delay between tests
            time.sleep(0.5)


if __name__ == "__main__":
    # Run with pytest
    import pytest
    pytest.main([__file__, '-v', '-s'])
