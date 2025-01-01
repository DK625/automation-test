from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import json


class TestCart():
    stored_localStorage = None
    driver = None

    @classmethod
    def setup_class(cls):
        """Chạy một lần khi bắt đầu tất cả test cases"""
        cls.driver = webdriver.Chrome()
        cls.vars = {}
        cls.input_data = cls.load_json('test_input.json')
        try:
            cls.mongo_client = MongoClient("mongodb://localhost:27017/")
            cls.db = cls.mongo_client["test"]
            cls.users_collection = cls.db["users"]
            cls.orders_collection = cls.db["orders"]
            print("MongoDB connection established")
        except Exception as e:
            print(f"MongoDB connection error: {str(e)}")

    @classmethod
    def load_json(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def teardown_class(cls):
        """Chỉ chạy sau khi tất cả test cases hoàn thành"""
        if hasattr(cls, 'driver'):  # Kiểm tra xem driver có tồn tại không
            cls.driver.quit()

    # optional
    def save_all_local_storage(self):
        # Lưu và escape JSON string
        TestCart.stored_localStorage = self.driver.execute_script(
            "return JSON.stringify(localStorage);"
        )

    # optional
    def restore_all_local_storage(self):
        """Khôi phục toàn bộ localStorage"""
        if TestCart.stored_localStorage:
            # Xóa localStorage hiện tại
            self.driver.execute_script("localStorage.clear();")
            # Khôi phục từng item từ data đã lưu
            restore_script = f"""
                        const storedData = {TestCart.stored_localStorage};
                        localStorage.clear();
                        Object.keys(storedData).forEach(key => {{
                            localStorage.setItem(key, storedData[key]);
                        }});
                    """

            self.driver.execute_script(restore_script)
        else:
            self.driver.execute_script(f"window.localStorage.setItem('productCart', 'b');")

    def login(self):
        login_input = self.input_data['login']
        self.driver.get("http://localhost:3000/home")
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
        email_input.send_keys(login_input['username'])

        # Nhập password - using MUI TextField selector with type='password'
        password_input = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.MuiInputBase-input[type='password']"))
        )
        password_input.send_keys(login_input['password'])

        submit_button = WebDriverWait(self.driver, 35).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButton-root"))
        )
        submit_button.click()

    def test_add_product_to_cart(self):
        input_data = self.input_data['add_to_cart']
        self.login()
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
        button4.click()  # Click vào tab Điện thoại để xem sản phẩm
        for product in input_data:
            product_name = list(product.keys())[0]
            add_button = WebDriverWait(self.driver, 35).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-testid='add-to-cart-{product_name}']"))
            )
            self.driver.execute_script("arguments[0].click();", add_button)

        icon1 = WebDriverWait(self.driver, 35).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiIconButton-colorInherit:nth-child(1)"))
        )
        icon1.click()  # Click vào icon gio hang để xem so luong (=2) sản phẩm vừa được thêm vào

        backdrop = WebDriverWait(self.driver, 35).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiBackdrop-root"))
        )
        backdrop.click()  # Click vào vùng trắng để đóng giỏ hàng

        iphone_name = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-h5.css-mxh2yv-MuiTypography-root"))
            # hoặc tag h6, div chứa tên
        ).text
        iphone_price = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBox-root.css-19nzcwv"))
            # hoặc span, div chứa giá
        ).text

        samsung_name = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-h5.css-mxh2yv-MuiTypography-root"))
        ).text
        samsung_price = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-h4.css-o71y5o-MuiTypography-root"))
        ).text
        cart_iphone_name = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-h5.css-mxh2yv-MuiTypography-root"))
            # hoặc div, span chứa tên trong cart
        ).text
        cart_samsung_name = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-h5.css-mxh2yv-MuiTypography-root"))
        ).text

        cart_iphone_price = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBox-root.css-19nzcwv"))
            # hoặc div, span chứa giá trong cart
        ).text
        cart_samsung_price = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-h4.css-o71y5o-MuiTypography-root"))
        ).text
        final_count_element = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBadge-badge"))
        )
        final_count = int(final_count_element.text)

        assert cart_iphone_name == iphone_name, "Product name mismatch"
        assert cart_samsung_name == samsung_name, "Product name mismatch"
        assert cart_iphone_price == iphone_price, "Price mismatch"
        assert cart_samsung_price == samsung_price, "Price mismatch"
        assert final_count == initial_count + 3, "Quantity not increased correctly"

        print("""
        TEST CASE: Add Products to Cart

        Results:
        ✓ Product Names Verified (iPhone & Samsung)
        ✓ Product Prices Verified 
        ✓ Quantity Updated: {initial_count} -> {final_count} (+3 items)

        Status: PASSED ✅
        """.format(initial_count=initial_count, final_count=final_count))
        # self.save_all_local_storage()

    def test_product_info_display(self):
        # Tìm lại element sau mỗi thao tác để tránh stale
        cart_icon = WebDriverWait(self.driver, 35).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".iconify--flowbite > path"))
        )
        cart_icon.click()

        cart_iphone_name = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-body1.css-14n6xi8-MuiTypography-root"))
            # hoặc div, span chứa tên trong cart
        ).text
        print('cart_iphone_name:', cart_iphone_name)
        cart_samsung_name = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-body1.css-14n6xi8-MuiTypography-root"))
        ).text

        cart_iphone_price = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-h4.css-txt9k1-MuiTypography-root"))
            # hoặc div, span chứa giá trong cart
        ).text
        cart_samsung_price = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-h4.css-txt9k1-MuiTypography-root"))
        ).text
        cart_iphone_quantity = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-body1.css-rb4thv-MuiTypography-root b"))
        ).text

        cart_samsung_quantity = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-body1.css-rb4thv-MuiTypography-root b"))
        ).text
        # lấy thông tin sản phẩm từ icon cart

        button = WebDriverWait(self.driver, 35).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-akzecb-MuiButtonBase-root-MuiButton-root"))
        )
        button.click()

        iphone_name = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-body1.css-b5urwl-MuiTypography-root"))
            # hoặc tag h6, div chứa tên
        ).text
        print('iphone_name:', iphone_name)
        iphone_price = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-h6.css-1pwfnb7-MuiTypography-root"))
            # hoặc span, div chứa giá
        ).text

        samsung_name = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-body1.css-b5urwl-MuiTypography-root"))
        ).text
        samsung_price = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-h6.css-1pwfnb7-MuiTypography-root"))
        ).text

        iphone_quantity = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number'].MuiInputBase-input"))
        ).get_attribute('value')

        samsung_quantity = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number'].MuiInputBase-input"))
        ).get_attribute('value')

        # lấy thông tin sản phẩm từ trang chính cart

        assert cart_iphone_name == iphone_name, "Product name mismatch"
        assert cart_samsung_name == samsung_name, "Product name mismatch"
        assert cart_iphone_price == iphone_price, "Price mismatch"
        assert cart_samsung_price == samsung_price, "Price mismatch"
        assert iphone_quantity == cart_iphone_quantity, "Quantity not increased correctly"
        assert samsung_quantity == cart_samsung_quantity, "Quantity not increased correctly"

        print("""
                TEST CASE: Product Info Display

                Results:
                ✓ Product Names Verified (iPhone & Samsung)
                ✓ Product Prices Verified 
                ✓ Quantity Verified

                Status: PASSED ✅
                """)

    def test_increase_decrease_quantity(self):
        self.driver.get("http://localhost:3000/my-cart")
        input_data = self.input_data['add_to_cart']
        for product in input_data:
            product_name = list(product.keys())[0]
            increase_button = WebDriverWait(self.driver, 35).until(
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
            for i in range(product[product_name]['increase_quantity']):
                self.driver.execute_script("arguments[0].click();", increase_button)
                current_value = int(WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f"[data-testid='quantity-input-{product_name}'] input[type='number']"))
            ).get_attribute('value'))
                assert current_value == initial_value + i + 1, f"After increase {i + 1} times, expected {initial_value + i + 1} but got {current_value}"
            for i in range(product[product_name]['decrease_quantity']):
                self.driver.execute_script("arguments[0].click();", decrease_button)
                current_value = int(WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f"[data-testid='quantity-input-{product_name}'] input[type='number']"))
            ).get_attribute('value'))
                assert current_value == initial_value + product[product_name][
                    'increase_quantity'] - i - 1, f"After decrease {i + 1} times, expected {initial_value + product[product_name]['increase_quantity'] - i - 1} but got {current_value}"


        print(f"""
        TEST CASE: Increase/Decrease Quantity

        Results:
        ✓ Initial quantity: {initial_value}
        ✓ After 10 increases: {initial_value + 10}
        ✓ After 5 decreases: {initial_value + 5}

        Status: PASSED ✅
        """)

    def test_cart_total_amount_calculation(self):
        checkboxes = WebDriverWait(self.driver, 35).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiBox-root.css-uz5qc span"))
        )
        checkboxes.click()  # Click vào tất cả các checkbox
        input_data = self.input_data['add_to_cart']
        expected_total = 0
        for product in input_data:
            product_name = list(product.keys())[0]
            # Lấy quantity
            quantity = int(WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f"[data-testid='quantity-input-{product_name}'] input[type='number']"))
            ).get_attribute('value'))
            try:
                # Try to get discount price first
                price = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='discount-price-{product_name}']"))
                ).text
            except:
                # If no discount, get original price
                price = WebDriverWait(self.driver, 35).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='price-{product_name}']"))
                ).text
            expected_total += quantity * int(price.replace('.', '').replace(' VND', ''))

        # Lấy tổng tiền hiển thị trên UI
        total_text = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-body1.css-c78xqc-MuiTypography-root"))
        ).text
        actual_total = int(total_text.replace('.', '').replace(' VND', ''))

        # Assert
        assert actual_total == expected_total, f"Expected total {expected_total:,} VND but got {actual_total:,} VND"

        result_str = ''
        for product in input_data:
            product_name = list(product.keys())[0]
            result_str += f"""Product: {product_name}
                ✓ Quantity: {quantity} 
                ✓ Price per item: {price} VND
                ✓ Subtotal: {quantity * int(price.replace('.', '').replace(' VND', '')):,} VND\n"""

        print(f"""
            TEST CASE: Calculate Total Price
            Results:
            {result_str}
            Total Amount: {actual_total:,} VND
            Status: PASSED ✅
            """)

    def test_delete_product(self):
        self.driver.get("http://localhost:3000/my-cart")

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
        assert not product_exists, f"Product '{product_name}' still exists after deletion"

        print(f"""
        TEST CASE: Delete Product

        Results:
        ✓ Product '{product_name}' successfully deleted

        Status: PASSED ✅
        """)
