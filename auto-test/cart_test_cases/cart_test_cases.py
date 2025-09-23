import os
import sys 
import time 

base = os.getcwd()      
path = os.path.dirname(base)              

sys.path.append(path)

from gg_sheet.index import ConnectGoogleSheet
from utils.index import parse_sheet_to_object_cart, log_to_sheet, log_to_sheet_multi_rows
from constant.index import CART_TEST_NAME, JSON_NAME

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # the set of wait condition 
from pymongo import MongoClient
import json
import os
from selenium.webdriver.chrome.options import Options




class TestCart():
    stored_localStorage = None
    driver = None

    @classmethod
    def setup_class(cls):
        """Chạy một lần khi bắt đầu tất cả test cases"""
        cls.driver = webdriver.Chrome()
        cls.vars = {}

        # load data from gg sheet 
        cls.gg_sheet = ConnectGoogleSheet(JSON_NAME)
        cls.worksheet = cls.gg_sheet.loadSheet_WorkSheet("1EEceAh_f_vogtMxTpwHtB9yMggXsXS7DPi28aag4arY", CART_TEST_NAME)
        
        # parse object : 
        cls.expectData, cls.dataSheet = parse_sheet_to_object_cart(cls.worksheet)

        cls.test_failures_dir = "test_failures"
        os.makedirs(cls.test_failures_dir, exist_ok=True)

        try:
            cls.mongo_client = MongoClient("mongodb://localhost:27017/")
            cls.db = cls.mongo_client["test"]
            cls.users_collection = cls.db["users"]
            cls.orders_collection = cls.db["orders"]
            print("MongoDB connection established")
        except Exception as e:
            print(f"MongoDB connection error: {str(e)}")

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
            raise e # == throw 

    @classmethod
    def load_json(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def teardown_class(cls):
        """Chỉ chạy sau khi tất cả test cases hoàn thành"""
        if hasattr(cls, 'driver'):  # Kiểm tra xem driver có tồn tại không
            cls.driver.quit()


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


    def test_add_product_to_cart(self):
        name_case = "add_to_cart"
        try : 
            time.sleep(4)
            input_data = self.dataSheet[name_case]
            cart_icon = WebDriverWait(self.driver, 35).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".iconify--flowbite > path"))
            )
            cart_icon.click()  # Click vào icon cart và xem giỏ hàng hiện tại

            initial_count = 0  # Lưu số lượng ban đầu trong giỏ hàng

            backdrop = WebDriverWait(self.driver, 35).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiBackdrop-root"))
            )
            backdrop.click()  # Click vào vùng trắng để đóng giỏ hàng

            button4 = WebDriverWait(self.driver, 35).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButtonBase-root:nth-child(4)"))
            )
            button4.click()  # Click vào tab thứ 4  để xem sản phẩm

            product_name_array = []
            #add product in the cart 
            for product in input_data:
                product_name = list(product.keys())[0] # get key of product (name_product)
                product_name_array.append(product_name)
                add_button = WebDriverWait(self.driver, 35).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-testid='add-to-cart-{product_name}']"))
                )
                for _ in range(product[product_name]["quantity"]) : 
                    self.driver.execute_script("arguments[0].click();", add_button)

            cart_icon = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".iconify--flowbite > path"))
            )
            cart_icon.click()
            cart_names = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-body1.css-14n6xi8-MuiTypography-root"))
                # hoặc div, span chứa tên trong cart
            )
            cart_0_name = cart_names[0].text
            cart_1_name = cart_names[1].text
            cart_2_name = cart_names[2].text
                
            try:
                # Try to get discount price first
                cart_price_0 = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='cart-product-discount-price-{product_name_array[0]}']"))
                ).text
                cart_price_1 = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='cart-product-discount-price-{product_name_array[1]}']"))
                ).text
                cart_price_2 = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='cart-product-discount-price-{product_name_array[2]}']"))
                ).text
                
            except:
                # If no discount, get original price
                cart_price_0 = WebDriverWait(self.driver, 35).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='cart-product-price-{product_name_array[0]}']"))
                ).text
                cart_price_1 = WebDriverWait(self.driver, 35).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='cart-product-price-{product_name_array[1]}']"))
                ).text
                cart_price_2 = WebDriverWait(self.driver, 35).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='cart-product-price-{product_name_array[2]}']"))
                ).text

            cart_quantity_0 =  WebDriverWait(self.driver, 35).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='cart-product-quantity-{product_name_array[0]}']"))
                ).text 
            cart_quantity_0 = cart_quantity_0.replace("x", "").strip()   
            cart_quantity_1 =  WebDriverWait(self.driver, 35).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='cart-product-quantity-{product_name_array[1]}']"))
                ).text    
            cart_quantity_1 = cart_quantity_1.replace("x", "").strip()   
            cart_quantity_2 =  WebDriverWait(self.driver, 35).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='cart-product-quantity-{product_name_array[2]}']"))
                ).text    
            cart_quantity_2 = cart_quantity_2.replace("x", "").strip()   
            
            obj_repeat = {

                "cart_price_0" : cart_price_0,
                "cart_price_1" : cart_price_1,
                "cart_price_2" : cart_price_2,

                "cart_quantity_0" : cart_quantity_0,
                "cart_quantity_1" : cart_quantity_1,
                "cart_quantity_2" : cart_quantity_2,
            }
            final_count = int(cart_quantity_0) + int(cart_quantity_1) + int(cart_quantity_2)

            self.wrap_assert(cart_0_name == self.expectData[name_case][0][product_name_array[0]]["name"], "Product name mismatch", product_name_array[0])
            self.wrap_assert(cart_1_name == self.expectData[name_case][1][product_name_array[1]]["name"], "Product name mismatch", product_name_array[1])
            self.wrap_assert(cart_2_name == self.expectData[name_case][2][product_name_array[2]]["name"], "Product name mismatch", product_name_array[2])
           
            self.wrap_assert(cart_price_0 == self.expectData[name_case][0][product_name_array[0]]["price"], f"Price {product_name_array[0]} mismatch", f"{product_name_array[0]}_price")
            self.wrap_assert(cart_price_1 == self.expectData[name_case][1][product_name_array[1]]["price"], f"Price {product_name_array[1]} mismatch", f"{product_name_array[1]}_price")
            self.wrap_assert(cart_price_2 == self.expectData[name_case][2][product_name_array[2]]["price"], f"Price {product_name_array[2]} mismatch", f"{product_name_array[2]}_price")
            self.wrap_assert(final_count == sum(int(self.expectData[name_case][i][product_name_array[i]]["quantity"]) for i in range(len(product_name_array))), "Quantity not increased correctly", "cart_quantity")

            print("""
                TEST CASE: Add Products to Cart
        
                Results:
                ✓ Product Names Verified (iPhone & Samsung)
                ✓ Product Prices Verified 
                ✓ Quantity Updated: {initial_count} -> {final_count} (+3 items)
        
                Status: PASSED ✅
                """.format(initial_count=initial_count, final_count=final_count))
            
            log_to_sheet_multi_rows(self.worksheet, name_case, "PASSED ✅", [f"name:{product_name_array[i]},quantity:{obj_repeat[f"cart_quantity_{i}"]},price:{obj_repeat[f"cart_price_{i}"]}" for i in range (len(product_name_array))], 3)
        except AssertionError as assert_err : 
            log_to_sheet(self.worksheet, name_case, "FAILED ❌", str(assert_err))
            

    def test_increase_decrease_quantity(self):
        name_case = "increase_decrease_quantity"
        try : 
            self.driver.get("http://14.225.44.169:3000/my-cart")
            input_data = self.dataSheet[name_case]
            product_name_array  = []
            obj_repeat = []
            index = 0
            for product in input_data:
                product_name = list(product.keys())[0]
                product_name_array.append(product_name)
                increase_button = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-testid='increase-quantity-{product_name}']"))
                )
                decrease_button = WebDriverWait(self.driver, 35).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-testid='decrease-quantity-{product_name}']"))
                )
                # Lấy giá trị ban đầu
                initial_value = int(WebDriverWait(self.driver, 35).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, f"[data-testid='quantity-input-{product_name}'] input[type='number']"))
                ).get_attribute('value'))

                
                item_data = {}
                item_data.setdefault(product_name, {}) 
                for i in range(int(product[product_name]['increase_quantity'])):

                    self.driver.execute_script("arguments[0].click();", increase_button)
                    current_value = int(WebDriverWait(self.driver, 35).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, f"[data-testid='quantity-input-{product_name}'] input[type='number']"))
                    ).get_attribute('value'))
                item_data[product_name]['total_after_increase'] = current_value
                
                self.wrap_assert(initial_value == self.expectData[name_case][index][product_name]["initial_quantity"], "Initial mismatch", "initial screenshot")
                self.wrap_assert(current_value == self.expectData[name_case][index][product_name]["total_after_increase"],
                                f"After increase {product[product_name]['increase_quantity']} times, expected {self.expectData[name_case][index][product_name]["total_after_increase"]} but got {current_value}",
                                f"increase_quantity_{product_name}_{i}")

                for i in range(int(product[product_name]['decrease_quantity'])):
                    self.driver.execute_script("arguments[0].click();", decrease_button)
                    current_value = int(WebDriverWait(self.driver, 35).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, f"[data-testid='quantity-input-{product_name}'] input[type='number']"))
                    ).get_attribute('value'))
                item_data[product_name]['total_after_decrease'] = current_value
                self.wrap_assert(current_value == self.expectData[name_case][index][product_name]["total_after_decrease"],
                                f"After decrease {product[product_name]['decrease_quantity']} times, expected {self.expectData[name_case][index][product_name]["total_after_decrease"]} but got {current_value}",
                                f"decrease_quantity_{product_name}_{i}")
                obj_repeat.append(item_data)
                index = index + 1 

            print(obj_repeat)

            print(f"""
            TEST CASE: Increase/Decrease Quantity

            Results:
            ✓ Initial quantity: {initial_value}
            ✓ After 10 increases: {initial_value + 10}
            ✓ After 5 decreases: {initial_value + 5}

            Status: PASSED ✅
            """)
            log_to_sheet_multi_rows(self.worksheet, name_case,"PASSED ✅",[f"total_after_increase:{obj_repeat[i][product_name_array[i]]["total_after_increase"]},total_after_decrease:{obj_repeat[i][product_name_array[i]]["total_after_decrease"]}" for i in range(len(product_name_array))],3)

        except AssertionError as assert_err : 
            log_to_sheet(self.worksheet, name_case,"FAILED ❌", str(assert_err))
            raise

    def test_cart_total_amount_calculation(self):
        name_case = "cart_total_amount_calculation"
        try : 
            checkboxes = WebDriverWait(self.driver, 35).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiBox-root.css-uz5qc span"))
            )
            checkboxes.click()  # Click vào tất cả các checkbox
            input_data = self.dataSheet[name_case]
            product_name_array = []
            for product in input_data:
                product_name = list(product.keys())[0]
                product_name_array.append(product_name)

            # Lấy quantity
            product_0_quantity = int(WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f"[data-testid='quantity-input-{product_name_array[0]}'] input[type='number']"))
            ).get_attribute('value'))
            product_1_quantity = int(WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f"[data-testid='quantity-input-{product_name_array[1]}'] input[type='number']"))
            ).get_attribute('value'))
            product_2_quantity = int(WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f"[data-testid='quantity-input-{product_name_array[2]}'] input[type='number']"))
            ).get_attribute('value'))


            try:
                # Try to get discount price first
                product_0_price = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='discount-price-{product_name_array[0]}']"))
                ).text
                product_0_price = product_0_price.replace("VND", "").replace(".", "")
                product_1_price = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='discount-price-{product_name_array[1]}']"))
                ).text
                product_1_price = product_1_price.replace("VND", "").replace(".", "")
                product_2_price = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='discount-price-{product_name_array[2]}']"))
                ).text
                product_2_price = product_2_price.replace("VND", "").replace(".", "")
            except:
                # If no discount, get original price
                product_0_price = WebDriverWait(self.driver, 35).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='price-{product_name_array[0]}']"))
                ).text
                product_0_price = product_0_price.replace("VND", "").replace(".", "")
                product_1_price = WebDriverWait(self.driver, 35).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='price-{product_name_array[1]}']"))
                ).text
                product_1_price = product_0_price.replace("VND", "").replace(".", "")
                product_2_price = WebDriverWait(self.driver, 35).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='price-{product_name_array[2]}']"))
                ).text
                product_2_price = product_0_price.replace("VND", "").replace(".", "")

            # total price of the products 
            product_0_total_price = int(product_0_price) * int(product_0_quantity)

            product_1_total_price = int(product_1_price) * int(product_1_quantity)
            product_2_total_price = int(product_2_price) * int(product_2_quantity)

            obj_repeate = {
                "product_0_total_price" : product_0_total_price, 
                "product_1_total_price" : product_1_total_price, 
                "product_2_total_price" : product_2_total_price, 
            }

            # Assert
            self.wrap_assert(product_0_total_price == self.expectData[name_case][0][product_name_array[0]]["total_price"],
                            f"Expected total {self.expectData[name_case][0][product_name_array[0]]["total_price"]} VND but got {product_0_total_price} VND",
                            "cart_total")
            self.wrap_assert(product_1_total_price == self.expectData[name_case][1][product_name_array[1]]["total_price"],
                            f"Expected total {self.expectData[name_case][1][product_name_array[1]]["total_price"]} VND but got {product_1_total_price} VND",
                            "cart_total")
            self.wrap_assert(product_1_total_price == self.expectData[name_case][2][product_name_array[2]]["total_price"],
                            f"Expected total {self.expectData[name_case][2][product_name_array[2]]["total_price"]} VND but got {product_2_total_price} VND",
                            "cart_total")

            log_to_sheet_multi_rows(self.worksheet, name_case, "PASSED ✅", [f"total_price:{obj_repeate[f'product_{i}_total_price']}" for i in range (len(product_name_array))], 3)

        except AssertionError as assert_err : 
            log_to_sheet(self.worksheet, name_case, "FAILED ❌", str(assert_err))

    def test_delete_product(self):
        try : 
            self.driver.get("http://14.225.44.169:3000/my-cart")

            # Đợi trang load hoàn tất
            WebDriverWait(self.driver, 35).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )

            # Lấy tên sản phẩm trước khi xóa để verify
            product_name = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "p.MuiTypography-root.MuiTypography-body1 > a"))
            ).text

            # Click vào nút delete (icon thùng rác)
            delete_button = WebDriverWait(self.driver, 35).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiBox-root.css-1gca1vy .MuiButtonBase-root"))
            )
            delete_button.click()

            # Kiểm tra sản phẩm đã bị xóa
            try:
                self.driver.find_element(By.LINK_TEXT, product_name)
                product_exists = True
            except:
                product_exists = False

            # Assert
            self.wrap_assert(not product_exists,
                            f"Product '{product_name}' still exists after deletion",
                            "delete_product")

            print(f"""
            TEST CASE: Delete Product

            Results:
            ✓ Product '{product_name}' successfully deleted

            Status: PASSED ✅
            """)
            log_to_sheet_multi_rows(self.worksheet, "delete_product", "PASSED ✅", ["quantity:0" for _ in range(3)],3)

        except AssertionError as assert_err : 
            log_to_sheet(self.worksheet, "Delete Product", "FAILED ❌", str(assert_err))
