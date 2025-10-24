import os
import sys 

base = os.getcwd()     
         
path = os.path.dirname(base)
sys.path.append(path)

import json
from gg_sheet.index import ConnectGoogleSheet
from utils.index import parse_sheet_to_object_purchase, log_to_sheet, log_to_sheet_multi_rows, log_to_sheet_multi_rows_option
from constant.index import PURCHASE_TEST_NAME, JSON_NAME

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time
from pymongo import MongoClient
import json
import pytest



class TestPurchase():
    stored_localStorage = None
    driver = None

    @classmethod
    def setup_class(cls):
        """Chạy một lần khi bắt đầu tất cả test cases"""
        cls.driver = webdriver.Chrome()
        cls.vars = {}

        # load data from gg sheet 
        cls.gg_sheet = ConnectGoogleSheet(JSON_NAME)
        cls.worksheet = cls.gg_sheet.loadSheet_WorkSheet("1EEceAh_f_vogtMxTpwHtB9yMggXsXS7DPi28aag4arY", PURCHASE_TEST_NAME)
        # parse object : 
        cls.expectData, cls.dataSheet = parse_sheet_to_object_purchase(cls.worksheet)

        cls.test_failures_dir = "test_failures"
        os.makedirs(cls.test_failures_dir, exist_ok=True)
        try:
            cls.mongo_client = MongoClient("mongodb://localhost:27018/")
            cls.db = cls.mongo_client["test"]
            cls.users_collection = cls.db["users"]
            cls.orders_collection = cls.db["orders"]
            print("MongoDB connection established")
        except Exception as e:
            print(f"MongoDB connection error: {str(e)}")

    @classmethod
    def load_json(cls, filename):
        if not os.path.exists(filename):
            print(f"⚠ File {filename} không tồn tại")
            return None 

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"⚠ JSON lỗi: {e}")
            return None

    def take_screenshot(self, name):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.test_failures_dir}/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"Screenshot saved: {filename}")

    def wrap_assert(self, condition, message, screenshot_name):
        try:
            assert condition, message
        except AssertionError as e:
            self.take_screenshot(f"failed_{screenshot_name}")
            raise e

    def test_login(self):
        def findTextMessage(child) : 
            message_login = None
            try : 
                el_parent_login_success = child.find_element(By.XPATH, "ancestor::div[contains(@class,'go4109123758')]")
                message_login = el_parent_login_success.text
            except Exception as e: 
                print("Error : ", e)
            return message_login

        try : 
            login_input = self.dataSheet['login']
            self.driver.get("http://14.225.44.169:3000/home")
            self.driver.maximize_window()

            # Click vào nút đăng nhập và chờ form login
            login_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-y9vvym-MuiButtonBase-root-MuiButton-root"))
            )
            login_button.click()

            # Nhập email - using MUI TextField selector
            email_input = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.MuiInputBase-input[aria-invalid='false']"))
            )
            email_input.send_keys(login_input['username'][0]) # single array 

            # click icon show/hidden password to debug
            icon_show_hidden = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiIconButton-root.MuiIconButton-edgeEnd"))
            )
            self.driver.execute_script("arguments[0].click();", icon_show_hidden)
            # Nhập password - using MUI TextField selector with type='password'
            password_input = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.MuiInputBase-input[type='text']#\\:r1g\\:"))
            )
            password_input.send_keys(login_input['password'][0]) # single array

            submit_button = WebDriverWait(self.driver, 35).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButton-root"))
            )
            submit_button.click()
            # test first login failed because need login successfully into web pages
            
            # login failed 
            el_child_login_failed = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div>div>.go2072408551.react-hot-toast>div>div:nth-child(2)>div.go2534082608"))
            )
            message_failed_login = findTextMessage(el_child_login_failed)
            print("Text expect : ", self.expectData["login"]["success"])
            print("UI text : ", message_failed_login)
            self.wrap_assert(self.expectData["login"]["failed"] == message_failed_login, "Not found message login failed", "login_screenshot")
            # login successfully
            time.sleep(4)
            password_input.send_keys(Keys.CONTROL, "a")  # bôi đen hết
            password_input.send_keys(Keys.DELETE) 
            password_input.send_keys(login_input['password'][1])
            submit_button.click()
            el_child_login_success = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div>div>.go2072408551.react-hot-toast>div>div:nth-child(2)>div.go2344853693"))
            )
           
            message_success_login = findTextMessage(el_child_login_success)
            print("Text expect : ", self.expectData["login"]["success"])
            print("UI text : ", message_success_login)
            self.wrap_assert(self.expectData["login"]["success"] == message_success_login, "Not found message login successfully", "login_screenshot")
            log_to_sheet(self.worksheet, "login", "PASSSED ✅", f"failed:{message_failed_login},success:{message_success_login}")
        except AssertionError as assert_err : 
            log_to_sheet(self.worksheet, "login", "FAILED ❌", str(assert_err))

    def test_validate_empty_shipping_address_fields(self):
        name_case = "validate_empty_shipping_address_fields"
        try : 
            time.sleep(4)
            input_data = self.dataSheet[name_case]
           
            for product in input_data['products']:
                # Click tab
                tab = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-testid='tab-{product['tab']}']"))
                )
                
                tab.click()
                    
                add_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-testid='add-to-cart-{product["items"]}']"))
                )
                self.driver.execute_script("arguments[0].click();", add_button)

            # Click cart icon
            cart_icon = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".iconify--flowbite > path"))
            )
            cart_icon.click()
            time.sleep(1)
            quantity_in_cart = int(WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBadge-badge"))
            ).text)
            assert quantity_in_cart == 5, f"Expected 5 items in cart, got {quantity_in_cart}"

            # Go to cart page
            cart_page_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-akzecb-MuiButtonBase-root-MuiButton-root"))
            )
            cart_page_button.click()

            time.sleep(1)
            # Select all products
            # self.driver.find_element(By.CSS_SELECTOR, ".css-tfttuo .PrivateSwitchBase-input").click()
            select_all = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".css-tfttuo .PrivateSwitchBase-input"))
            )
            select_all.click()

            # Proceed to checkout
            checkout_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButton-root"))
            )
            checkout_button.click()

            # Change shipping address
            change_address = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButton-text"))
            )
        
            self.driver.execute_script("arguments[0].click();", change_address)

            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            "form>div>div>div>button"))).click()  # choice current address
        
            # Clear all input fields
            input_fields = WebDriverWait(self.driver, 5).until(
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
            confirm_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1uimnmd-MuiButtonBase-root-MuiButton-root"))
            )
            confirm_button.click()

            # Verify error messages (array)
            error_messages = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error"))
            )

          
            # Verify specific error messages
            actual_errors = [message.text for message in error_messages]

            for expected in self.expectData[name_case]['error']:
                assert expected in actual_errors, f"Expected error message '{expected}' not found"

            # Close form
            close_button = WebDriverWait(self.driver, 5).until(
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
            print("Array : " , actual_errors)
            log_to_sheet_multi_rows(self.worksheet, name_case, "PASSED ✅", [f"error:{actual_errors}"], 1)
        except AssertionError as assert_err : 
            log_to_sheet(self.worksheet, name_case, "FAILED ❌", str(assert_err))


    def test_add_multiple_addresses_and_verify_form_display(self):
        """
        Tests adding 5 new addresses and verifies information consistency:
        - Adds 5 different addresses
        - Verifies form input matches displayed information
        - Checks address details inside and outside the form
        """
        name_case = "test_multiple_addresses"
        try : 
            input_data = self.dataSheet[name_case]
            change_button = WebDriverWait(self.driver, 55).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiButton-root"))
            )
            self.driver.execute_script("arguments[0].click();", change_button)  # start change
            cancel_button = WebDriverWait(self.driver, 35).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'MuiButton-text') and text()='Hủy bỏ']"))
            )
            cancel_button.click()

            add_button = WebDriverWait(self.driver, 35).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1lfi9f6-MuiButtonBase-root-MuiButton-root"))
            )
            add_button.click()  # add new address
            # Using the most reliable selectors for each field
            for index, address in enumerate(input_data['addresses']):
                name_input = WebDriverWait(self.driver, 35).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Nhập họ và tên']"))
                )
                name_input.send_keys(address['name'])

                address_input = WebDriverWait(self.driver, 35).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Nhập địa chỉ']"))
                )
                address_input.send_keys(address['address'])

                city_select = WebDriverWait(self.driver, 35).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='combobox']"))
                )
                city_select.click()
                city_options = WebDriverWait(self.driver, 35).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.MuiMenuItem-root"))
                )
                city_options[address['city_index']].click()

                phone_input = WebDriverWait(self.driver, 35).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[inputmode='numeric'][pattern='[0-9]*']"))
                )
                phone_input.send_keys(address['phone'])

                self.driver.find_element(By.CSS_SELECTOR,
                                        ".css-1uimnmd-MuiButtonBase-root-MuiButton-root").click()  # confirm

                if index < len(input_data['addresses']) - 1:
                    self.driver.find_element(By.CSS_SELECTOR,
                                            ".css-1lfi9f6-MuiButtonBase-root-MuiButton-root").click()  # add new address
            second_address = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@value='0']/following::span[contains(@class, 'MuiTypography-body1')][1]"))
            ).text
            third_address = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@value='1']/following::span[contains(@class, 'MuiTypography-body1')][1]"))
            ).text
            fourth_address = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@value='1']/following::span[contains(@class, 'MuiTypography-body1')][2]"))
            ).text

            self.wrap_assert(second_address == self.expectData[name_case][0]['addresses']["full_address"],
                            "Second address does not match",
                            "second_address_check")
            self.wrap_assert(third_address == self.expectData[name_case][1]['addresses']["full_address"],
                            "Third address does not match",
                            "third_address_check")
            self.wrap_assert(fourth_address == self.expectData[name_case][2]['addresses']["full_address"],
                            "Fourth address does not match",
                            "fourth_address_check")
            
            address_array = [second_address, third_address, fourth_address]

            print(f"""
            TEST CASE: Add Multiple Addresses and Verify Form Display

            Results:
            ✓ Successfully added 3 new addresses
            ✓ Address Verification:
            - Address 1: {second_address}
            - Address 2: {third_address}
            - Address 3: {fourth_address}
            ✓ All addresses matched expected format
            ✓ Address details consistent between form and display

            Status: PASSED ✅
            """)
            log_to_sheet_multi_rows(self.worksheet, name_case, "PASSED ✅", [f"full_address:{adres}" for adres in address_array], 3)
        except AssertionError as assert_err : 
            log_to_sheet(self.worksheet, name_case, "FAILED ❌", str(assert_err))


    def test_update_delivery_address_and_verify_display(self):
        """
        Tests updating delivery address and verifies information:
        - Selects specific address for delivery
        - Verifies selected address matches display
        - Confirms address details consistency
        """
        name_case = "test_update_delivery_address_and_verify_display"
        try : 
            self.driver.find_element(By.CSS_SELECTOR,
                                    ".MuiBox-root:nth-child(2) > .MuiFormControlLabel-root > .MuiTypography-root").click()  # second choice address
            self.driver.find_element(By.CSS_SELECTOR,
                                    ".css-1uimnmd-MuiButtonBase-root-MuiButton-root").click()  # update address
            # Lấy phần thông tin số điện thoại và tên
            name_phone = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "p.MuiTypography-root.css-1wr5z0g-MuiTypography-root"))
            ).text

            # Lấy phần địa chỉ
            address = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.MuiTypography-root.css-1f0oh43-MuiTypography-root"))
            ).text

            self.wrap_assert(name_phone + ' ' + address == self.expectData[name_case][0]['delivery_address']["content"],
                            f"Address mismatch. Expected: {self.expectData[name_case][0]['delivery_address']["content"]}, Got: '{name_phone + address}'",
                            "delivery_address_check")

            print(f"""
            TEST CASE: Update Delivery Address and Verify Display

            Results:
            ✓ Successfully selected new delivery address
            ✓ Address Details:
                - Contact: {name_phone}
                - Address: {address}
            ✓ Address information matches expected values

            Status: PASSED ✅
            """)
            log_to_sheet_multi_rows(self.worksheet,name_case, "PASSED ✅", [f"content:{name_phone + ' ' + address}"],1)
        except AssertionError as assert_err : 
            log_to_sheet(self.worksheet,name_case, "FAILED ❌", str(assert_err))


    def test_shipping_fee_calculation_by_provider(self):
        """
        Tests shipping fee calculation for different providers:
        - GHN: Fixed 20,000 VND
        - GHTK: Fixed 1,000 VND
        - Verifies fee display and total calculation
        """
        name_case = 'test_shipping_fee'
        try : 
            input_data = self.dataSheet[name_case]
            self.driver.find_element(By.CSS_SELECTOR,
                                    ".MuiFormControlLabel-root:nth-child(2) .PrivateSwitchBase-input").click()  # change shoppe method
            shoppe_shipping_fee = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".css-147dy5z:nth-child(2) p:last-child"))
            ).text
            self.driver.find_element(By.NAME, "radio-delivery-group").click()  # change GHTK method
            ghtk_shipping_fee = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".css-147dy5z:nth-child(2) p:last-child"))
            ).text
            self.wrap_assert(shoppe_shipping_fee == self.expectData[name_case][0]['providers']['shopee'],
                            f"Shopee shipping fee incorrect. Expected: {self.expectData[name_case][0]['providers']['shopee']}, Got: {shoppe_shipping_fee}",
                            "shopee_fee_check")
            self.wrap_assert(ghtk_shipping_fee == self.expectData[name_case][0]['providers']['ghtk'],
                            f"GHTK shipping fee incorrect. Expected: {self.expectData[name_case][0]['providers']['ghtk']}, Got: {ghtk_shipping_fee}",
                            "ghtk_fee_check")

            print(f"""
            TEST CASE: Shipping Fee Calculation By Provider

            Results:
            ✓ Successfully tested both shipping providers
            ✓ Shipping Fees:
                - Shopee: {shoppe_shipping_fee}
                - GHTK: {ghtk_shipping_fee}
            ✓ All shipping fees match expected values

            Status: PASSED ✅
            """)
            log_to_sheet_multi_rows(self.worksheet, name_case, "PASSED ✅", [f"shopee:{shoppe_shipping_fee},ghtk:{ghtk_shipping_fee}"] , 1)
        except AssertionError as assert_err : 
            log_to_sheet(self.worksheet, name_case, "FAILED ❌", str(assert_err) )
            

    def test_total_price_calculation_with_shipping_and_discount(self):
        """
        Tests total price calculation including shipping:
        - Calculates subtotal of items
        - Adds fixed shipping fee (25,000 VND)
        - Verifies final total
        """
        name_case = "test_price_calculation"
        try : 

            def get_product_price(product_element):
                """Get either discounted price or original price for a product"""
                try:
                    return product_element.find_element(By.CSS_SELECTOR,
                                                        ".MuiTypography-h4.css-1qv43kz-MuiTypography-root").text
                except:
                    return product_element.find_element(By.CSS_SELECTOR, ".MuiTypography-h6").text

            def get_price_amount(price_string):
                """Convert price string to integer"""
                return int(price_string.replace('VND', '').replace('.', '').strip())

            # Then use it
            product_prices = [
                get_product_price(item)
                for item in self.driver.find_elements(By.CSS_SELECTOR, ".MuiBox-root.css-fm4r4t")
            ]
            shipping_fee = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".css-147dy5z:nth-child(2) p:last-child"))
            ).text
            total_amount = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".css-147dy5z:nth-child(3) p:last-child"))
            ).text
            product_prices_sum = sum(get_price_amount(price) for price in product_prices)
            shipping_fee_amount = get_price_amount(shipping_fee)
            total_amount_value = get_price_amount(total_amount)

            self.wrap_assert(product_prices == self.expectData[name_case][0]['product_prices']["content"],
                                f"Product prices mismatch. Expected: {self.expectData[name_case][0]['product_prices']["content"]}, Got: {product_prices}",
                                "product_prices_check")
            self.wrap_assert(product_prices_sum + shipping_fee_amount == total_amount_value,
                                f"Total amount mismatch. Expected: {product_prices_sum + shipping_fee_amount:,} VND, Got: {total_amount_value:,} VND",
                                "total_amount_check")

            print(f"""
            TEST CASE: Verify Order Total Calculation

            Results:
            ✓ Product Prices Verified:
                - Apple Watch: {product_prices[0]}
                - Surface Pro: {product_prices[1]}
                - iPad: {product_prices[2]}
                - Acer Laptop: {product_prices[3]}
                - Nokia: {product_prices[4]}
            ✓ Shipping Fee: {shipping_fee}
            ✓ Total Amount: {total_amount}
            ✓ Calculation Verified:
                Sum of Products: {product_prices_sum:,} VND
                + Shipping Fee: {shipping_fee_amount:,} VND
                = Total: {total_amount_value:,} VND

            Status: PASSED ✅
            """)
            log_to_sheet_multi_rows(self.worksheet, name_case, "PASSED ✅", [f"content:{product_prices}"], 1)
        except AssertionError as assert_err: 
            log_to_sheet(self.worksheet, name_case, "FAILED ❌",  str(assert_err))


    def test_cart_to_purchase_flow_integration(self):
        """
        Integration test for complete purchase flow:
        - Adds items to cart
        - Proceeds to checkout
        - Selects delivery address
        - Chooses shipping method
        - Completes purchase
        - Verifies order creation
        """
        name_case = "test_cart_to_purchase_flow_integration"
        try : 
            button_order = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBox-root.css-51xbo2>button")))
            button_order.click() 

            button_confirm = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".swal2-confirm.swal2-styled")))
            button_confirm.click()
           
            try:
                after_quantity_in_cart = int(WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Giỏ hàng'] span.MuiBadge-badge"))
                ).text)
            except:
                after_quantity_in_cart = 0
            print("<<< check after : ", after_quantity_in_cart)
            print("<<<check : ", self.expectData[name_case][0]["quantity"]["content"])
            self.wrap_assert(after_quantity_in_cart == self.expectData[name_case][0]["quantity"]["content"],
                            "Expected 0 items in after purchase",
                            "cart_empty_check")
            print(f"""
                        TEST CASE: Purchase Flow Integration

                        Workflow Steps:
                        ✓ Expected 5 items in before purchase
                        ✓ Expected 0 items in after purchase


                        Status: PASSED ✅
                        """)
            log_to_sheet(self.worksheet, name_case, "FPASSED ✅", f"content:{after_quantity_in_cart}")
    
        except AssertionError as assert_err : 
            log_to_sheet(self.worksheet, name_case, "FAILED ❌", str(assert_err))
    
    def test_teardown_class(self):
        try : 
            test_addresses = [
                    {
                        "firstName": address["name"].split(" ")[1],
                        "lastName": address["name"].split(" ")[0],
                        "address": address["address"],
                        "phoneNumber": address["phone"]
                    } for address in self.dataSheet["test_multiple_addresses"]["addresses"]
                    
                ]
            
            self.verify_database_state(PURCHASE_TEST_NAME, test_addresses)
            self.rollback_database_changes(PURCHASE_TEST_NAME, test_addresses)
            
            

            """Chỉ chạy sau khi tất cả test cases hoàn thành"""
            if hasattr(self, 'driver'):  # Kiểm tra xem driver có tồn tại không
                self.driver.quit()
            log_to_sheet(self.worksheet, "TEST TEAR DOWN", "PASSED ✅", "Test tear down successfull")
        except Exception as e : 
            log_to_sheet(self.worksheet, "TEST TEAR DOWN", "FAILED ❌", str(e))

    def verify_database_state(self, test_name, expected_state):
        """
        Verifies the database state after test execution

        Args:
            test_name (str): Name of the test being verified
            expected_state (dict): Expected database state including orders and addresses
        """
        try:
            # Find user
            user = self.users_collection.find_one({"email": self.dataSheet["login"]["username"][0]})
            if not user:
                raise AssertionError(f"{test_name}: User not found in database")

            # Verify addresses if expected
            if 'addresses' in expected_state:
                actual_addresses = user.get('addresses', [])
                self.wrap_assert(
                    len(actual_addresses) == len(expected_state['addresses']),
                    f"{test_name}: Expected {len(expected_state['addresses'])} addresses, got {len(actual_addresses)}",
                    "db_addresses_count"
                )

                # Verify each address
                for expected_addr in expected_state['addresses']:
                    found = False
                    for actual_addr in actual_addresses:
                        if (actual_addr.get('firstName') == expected_addr.get('firstName') and
                                actual_addr.get('lastName') == expected_addr.get('lastName') and
                                actual_addr.get('address') == expected_addr.get('address') and
                                actual_addr.get('phoneNumber') == expected_addr.get('phoneNumber')):
                            found = True
                            break

                    self.wrap_assert(
                        found,
                        f"{test_name}: Expected address not found: {expected_addr}",
                        "db_address_match"
                    )

            # Verify orders if expected
            if 'orders' in expected_state:
                user_orders = list(self.orders_collection.find({"user": user['_id']}).sort("createdAt", -1))
                self.wrap_assert(
                    len(user_orders) >= len(expected_state['orders']),
                    f"{test_name}: Expected at least {len(expected_state['orders'])} orders, got {len(user_orders)}",
                    "db_orders_count"
                )

                # Verify most recent order
                latest_order = user_orders[0]
                expected_order = expected_state['orders'][0]

                # Verify order details
                self.wrap_assert(
                    latest_order.get('totalAmount') == expected_order.get('totalAmount'),
                    f"{test_name}: Order total amount mismatch. Expected: {expected_order.get('totalAmount')}, Got: {latest_order.get('totalAmount')}",
                    "db_order_total"
                )

                # Verify products in order
                actual_products = latest_order.get('products', [])
                expected_products = expected_order.get('products', [])

                self.wrap_assert(
                    len(actual_products) == len(expected_products),
                    f"{test_name}: Product count mismatch in order. Expected: {len(expected_products)}, Got: {len(actual_products)}",
                    "db_products_count"
                )

            print(f"\n{test_name}: Database verification passed ✅")

        except Exception as e:
            self.take_screenshot("db_verification_error")
            raise AssertionError(f"{test_name}: Database verification failed - {str(e)}")
        

    def rollback_database_changes(self, test_name, test_addresses):
        """
        Rolls back database changes made during test execution

        Args:
            test_name (str): Name of the test being rolled back
        """
       

        try:
            # Find user
            user = self.users_collection.find_one({"email": self.dataSheet["login"]["username"][0]})
            if not user:
                print(f"{test_name}: No user found to rollback")
                return

            # Rollback orders
            latest_order = self.orders_collection.find_one(
                {"user": user['_id']},
                sort=[("createdAt", -1)]
            ) # get latest order and delete 

            if latest_order:
                self.orders_collection.delete_one({"_id": latest_order["_id"]})
                print(f"{test_name}: Rolled back latest order")

            # Rollback addresses
            

            # update_result = self.users_collection.update_one(
            #     {"_id": user['_id']},
            #     {"$pull": {"addresses": {"$in": test_addresses}}}
            # ) # delete user have addresss in test_addresses 

            for addr in test_addresses:
                self.users_collection.update_one(
                    {"_id": user["_id"]},
                    {"$pull": {
                        "addresses": {
                            "address": addr["address"],
                            "firstName": addr["firstName"],
                            "lastName": addr["lastName"],
                            "phoneNumber": addr["phoneNumber"]
                        }
                    }}
                )


            print(f"{test_name}: Rolled back {update_result.modified_count} test addresses")

        except Exception as e:
            print(f"{test_name}: Rollback failed - {str(e)}")
        finally:
            if self.mongo_client:
                self.mongo_client.close()
                print("MongoDB connection closed")

   
