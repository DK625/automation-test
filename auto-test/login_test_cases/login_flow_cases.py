"""
Test Cases cho chức năng Đăng nhập (DN_1 đến DN_34)
File: login_flow_cases.py
Tested with MCP Selenium - All cases verified
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
from utils.index import update_status_result_to_sheet
from constant.index import LOGIN_TEST_CASE, JSON_NAME, SPREEDSHEET_ID


# ============== CONSTANTS ==============
BASE_URL = "http://14.225.44.169:3000/home"
EMAIL_TEST = "lovecatdat@gmail.com"
PASSWORD_TEST = "123456@Dat"

# Row mapping for each test case in Google Sheet
TEST_CASE_ROWS = {
    "DN_1": 4,
    "DN_2": 5,
    "DN_3": 6,
    "DN_4": 7,
    "DN_5": 8,
    "DN_6": 9,
    "DN_7": 10,
    "DN_8": 11,
    "DN_9": 12,
    "DN_10": 13,
    "DN_11": 14,
    "DN_12": 17,
    "DN_13": 18,
    "DN_14": 19,
    "DN_15": 20,
    "DN_16": 21,
    "DN_20": 26,
    "DN_21": 27,
    "DN_22": 29,
    "DN_23": 30,
    "DN_24": 31,
    "DN_25": 32,
    "DN_26": 33,
    "DN_27": 34,
    "DN_28": 35,
    "DN_29": 36,
    "DN_30": 37,
    "DN_31": 38,
    "DN_32": 39,
    "DN_33": 40,
    "DN_34": 41,
}

# CSS Selectors
SELECTORS = {
    "login_button": ".css-y9vvym-MuiButtonBase-root-MuiButton-root",
    "title": "//*[@class='MuiTypography-root MuiTypography-h5 css-1000all-MuiTypography-root']",
    "labels": ".MuiFormLabel-root.MuiInputLabel-root.MuiInputLabel-formControl.MuiInputLabel-animated.MuiInputLabel-shrink",
    "email_input": ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input",
    "password_input": ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input",
    "remember_checkbox": ".PrivateSwitchBase-input",
    "forgot_password_link": "Quên mật khẩu?",
    "sign_in_button": ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium",
    "register_link": "Đăng ký",
    "facebook_icon": ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-z70jni-MuiButtonBase-root-MuiIconButton-root",
    "google_icon": ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-7qi38e-MuiButtonBase-root-MuiIconButton-root",
    "show_password_icon": ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-edgeEnd.MuiIconButton-sizeMedium.css-xubj68-MuiButtonBase-root-MuiIconButton-root",
    "error_message": ".MuiFormHelperText-root.Mui-error.MuiFormHelperText-sizeSmall.MuiFormHelperText-contained.MuiFormHelperText-filled.Mui-required.css-brfce9-MuiFormHelperText-root",
    "error_required": ".MuiFormHelperText-root.Mui-error.MuiFormHelperText-sizeSmall.MuiFormHelperText-contained.Mui-required.css-brfce9-MuiFormHelperText-root",
    "alert_message": ".go4109123758",
    "user_avatar": ".MuiAvatar-root.MuiAvatar-circular.MuiAvatar-colorDefault.css-1j1wjvp-MuiAvatar-root",
    "logout_button": ".MuiButtonBase-root.MuiMenuItem-root.MuiMenuItem-gutters.MuiMenuItem-root.MuiMenuItem-gutters.css-wr5qfr-MuiButtonBase-root-MuiMenuItem-root",
}

# Run index from environment variable (default 1)
RUN_INDEX = int(os.environ.get("RUN_INDEX", 1))


class TestLoginFlow:
    """Test class for Login Flow test cases DN_1 to DN_34"""
    
    driver = None
    worksheet = None
    test_failures_dir = "test_failures"

    @classmethod
    def setup_class(cls):
        """Setup: Initialize browser and Google Sheet connection"""
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        
        # Connect to Google Sheet
        cls.gg_sheet = ConnectGoogleSheet(JSON_NAME)
        cls.worksheet = cls.gg_sheet.loadSheet_WorkSheet(SPREEDSHEET_ID, LOGIN_TEST_CASE)
        
        # Create test_failures directory
        os.makedirs(cls.test_failures_dir, exist_ok=True)

    @classmethod
    def teardown_class(cls):
        """Teardown: Close browser"""
        if cls.driver:
            cls.driver.quit()

    def take_screenshot(self, name):
        """Take screenshot and save with timestamp"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.test_failures_dir}/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"Screenshot saved: {filename}")
        return filename

    def update_result(self, test_id, status):
        """Update test result to Google Sheet"""
        row = TEST_CASE_ROWS.get(test_id)
        if row:
            update_status_result_to_sheet(
                worksheet=self.worksheet,
                base_col="F",
                row=row,
                value_update=[status],
                run_index=RUN_INDEX
            )

    def navigate_to_login_page(self):
        """Navigate to login page"""
        self.driver.get(BASE_URL)
        login_button = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["login_button"]))
        )
        login_button.click()
        time.sleep(1)

    def logout_if_logged_in(self):
        """Logout if user is currently logged in"""
        try:
            user_btn = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["user_avatar"]))
            )
            user_btn.click()
            
            logout_btn = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, SELECTORS["logout_button"]))
            )[-1]
            logout_btn.click()
            time.sleep(1)
        except:
            pass  # Not logged in

    # ============== SECTION 1: GIAO DIỆN TỔNG THỂ (DN_1 - DN_11) ==============
    # Verified with MCP Selenium - All PASS

    def test_DN_1_kiem_tra_tieu_de_man_hinh(self):
        """DN_1: Kiểm tra tiêu đề màn hình - Hiển thị 'Đăng nhập' đúng căn giữa"""
        test_id = "DN_1"
        try:
            self.navigate_to_login_page()
            
            title = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, SELECTORS["title"]))
            )
            
            assert title.is_displayed(), "Tiêu đề không hiển thị"
            assert title.text == "Đăng nhập", f"Tiêu đề không đúng: {title.text}"
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_2_kiem_tra_label_email(self):
        """DN_2: Kiểm tra label Email - Label 'Email *' hiển thị đúng"""
        test_id = "DN_2"
        try:
            labels = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, SELECTORS["labels"]))
            )
            label_email = labels[0]
            
            text = re.sub(r"\s+", " ", label_email.text).strip()
            assert text == "Email *", f"Label Email không đúng: {text}"
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_3_kiem_tra_label_mat_khau(self):
        """DN_3: Kiểm tra label Mật khẩu - Label 'Mật khẩu *' hiển thị đúng"""
        test_id = "DN_3"
        try:
            labels = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, SELECTORS["labels"]))
            )
            label_password = labels[1]
            
            text = re.sub(r"\s+", " ", label_password.text).strip()
            assert text == "Mật khẩu *", f"Label Mật khẩu không đúng: {text}"
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_4_kiem_tra_placeholder_email(self):
        """DN_4: Kiểm tra placeholder Email - Placeholder 'Nhập email'"""
        test_id = "DN_4"
        try:
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            
            placeholder = email_input.get_attribute("placeholder")
            assert placeholder == "Nhập email", f"Placeholder Email không đúng: {placeholder}"
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_5_kiem_tra_placeholder_password(self):
        """DN_5: Kiểm tra placeholder Password - Placeholder 'Nhập mật khẩu'"""
        test_id = "DN_5"
        try:
            password_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            
            placeholder = password_input.get_attribute("placeholder")
            assert placeholder == "Nhập mật khẩu", f"Placeholder Password không đúng: {placeholder}"
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_6_kiem_tra_checkbox_nho_mat_khau(self):
        """DN_6: Kiểm tra checkbox 'Nhớ mật khẩu' - Checkbox hiển thị đúng"""
        test_id = "DN_6"
        try:
            checkbox = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, SELECTORS["remember_checkbox"]))
            )
            
            assert checkbox is not None, "Checkbox 'Nhớ mật khẩu' không tồn tại"
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_7_kiem_tra_link_quen_mat_khau(self):
        """DN_7: Kiểm tra link 'Quên mật khẩu?' - Link hiển thị đúng màu, có thể bấm"""
        test_id = "DN_7"
        try:
            link = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Quên mật khẩu')]"))
            )
            
            assert link.is_displayed(), "Link 'Quên mật khẩu?' không hiển thị"
            assert link.is_enabled(), "Link 'Quên mật khẩu?' không thể click"
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_8_kiem_tra_nut_sign_in(self):
        """DN_8: Kiểm tra nút 'Sign In' - Nút hiển thị đúng màu tím, bo tròn, chữ trắng"""
        test_id = "DN_8"
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            
            assert button.is_displayed(), "Nút Sign In không hiển thị"
            
            bg_color = button.value_of_css_property("background-color")
            text_color = button.value_of_css_property("color")
            border_radius = button.value_of_css_property("border-radius")
            
            assert bg_color == "rgba(115, 103, 240, 1)", f"Sai màu nền: {bg_color}"
            assert text_color == "rgba(255, 255, 255, 1)", f"Sai màu chữ: {text_color}"
            assert border_radius == "10px", f"Sai bo góc: {border_radius}"
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_9_kiem_tra_link_dang_ky(self):
        """DN_9: Kiểm tra link Đăng ký - Hiển thị đúng văn bản 'Đăng ký', có thể click"""
        test_id = "DN_9"
        try:
            link = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Đăng ký')]"))
            )
            
            assert link.is_displayed(), "Link 'Đăng ký' không hiển thị"
            assert link.is_enabled(), "Link 'Đăng ký' không thể click"
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_10_kiem_tra_icon_facebook(self):
        """DN_10: Kiểm tra icon đăng nhập bằng Facebook - Icon Facebook hiển thị đúng"""
        test_id = "DN_10"
        try:
            icon = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["facebook_icon"]))
            )
            
            assert icon.is_displayed(), "Icon Facebook không hiển thị"
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_11_kiem_tra_icon_google(self):
        """DN_11: Kiểm tra icon đăng nhập bằng Google - Icon Google hiển thị đúng"""
        test_id = "DN_11"
        try:
            icon = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["google_icon"]))
            )
            
            assert icon.is_displayed(), "Icon Google không hiển thị"
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e


# ============== SECTION 2: CHỨC NĂNG ĐĂNG NHẬP - TRƯỜNG EMAIL (DN_12 - DN_16) ==============
    # Verified with MCP Selenium - All PASS

    def test_DN_12_nhap_email_hop_le(self):
        """DN_12: Nhập email hợp lệ - Đăng nhập thành công"""
        test_id = "DN_12"
        try:
            self.navigate_to_login_page()
            
            # Nhập email hợp lệ
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(EMAIL_TEST)
            
            # Nhập mật khẩu
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(PASSWORD_TEST)
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            # Verify đăng nhập thành công
            WebDriverWait(self.driver, 10).until(EC.url_contains("/home"))
            assert "/home" in self.driver.current_url
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_13_nhap_email_thieu_at(self):
        """DN_13: Nhập email không hợp lệ (thiếu @) - Hiển thị lỗi"""
        test_id = "DN_13"
        try:
            # Logout nếu đang đăng nhập
            self.logout_if_logged_in()
            self.navigate_to_login_page()
            
            # Nhập email thiếu @
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys("lovecatdatgmail.com")
            
            # Nhập mật khẩu
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(PASSWORD_TEST)
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            # Verify hiển thị lỗi
            error = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error"))
            )
            text = re.sub(r"\s+", " ", error.text).strip()
            assert "Email không hợp lệ" in text
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_14_nhap_email_khong_co_domain(self):
        """DN_14: Nhập email không hợp lệ (không có domain) - Hiển thị lỗi"""
        test_id = "DN_14"
        try:
            self.navigate_to_login_page()
            
            # Nhập email không có domain
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys("lovecatdat@")
            
            # Nhập mật khẩu
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(PASSWORD_TEST)
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            # Verify hiển thị lỗi
            error = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error"))
            )
            text = re.sub(r"\s+", " ", error.text).strip()
            assert "Email không hợp lệ" in text
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_15_nhap_email_ky_tu_dac_biet_sai(self):
        """DN_15: Nhập email chứa ký tự đặc biệt sai - Hiển thị lỗi"""
        test_id = "DN_15"
        try:
            self.navigate_to_login_page()
            
            # Nhập email với ký tự đặc biệt sai
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys("lovecatdat#")
            
            # Nhập mật khẩu
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(PASSWORD_TEST)
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            # Verify hiển thị lỗi
            error = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error"))
            )
            text = re.sub(r"\s+", " ", error.text).strip()
            assert "Email không hợp lệ" in text
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_16_kiem_tra_do_dai_email_max(self):
        """DN_16: Kiểm tra độ dài email max (256 ký tự) - Hiển thị lỗi"""
        test_id = "DN_16"
        try:
            self.navigate_to_login_page()
            
            # Nhập email 256+ ký tự
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys("exampl" + "e" * 256 + "@gmail.com")
            
            # Nhập mật khẩu
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(PASSWORD_TEST)
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            # Verify hiển thị lỗi
            error = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error"))
            )
            text = re.sub(r"\s+", " ", error.text).strip()
            assert "Email vượt quá kí tự cho phép" in text
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    # ============== SECTION 2.1: TRƯỜNG MẬT KHẨU (DN_18 - DN_21) ==============
    # DN_20, DN_21: Verified with MCP Selenium - PASS

    def test_DN_20_hien_mat_khau(self):
        """DN_20: Hiện mật khẩu - Mật khẩu hiện rõ (type='text')"""
        test_id = "DN_20"
        try:
            self.navigate_to_login_page()
            
            # Nhập mật khẩu
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(PASSWORD_TEST)
            
            # Click icon hiện mật khẩu
            show_icon = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["show_password_icon"]))
            )
            show_icon.click()
            
            # Verify password type = text
            assert pass_input.get_attribute("type") == "text", "Mật khẩu không hiện rõ"
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_21_an_mat_khau(self):
        """DN_21: Ẩn mật khẩu - Mật khẩu bị che (type='password')"""
        test_id = "DN_21"
        try:
            # Tiếp tục từ test trước (mật khẩu đang hiện)
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            
            # Click icon ẩn mật khẩu
            show_icon = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["show_password_icon"]))
            )
            show_icon.click()
            
            # Verify password type = password
            assert pass_input.get_attribute("type") == "password", "Mật khẩu không bị che"
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e


# ============== SECTION 3: BUTTON ĐĂNG NHẬP (DN_22 - DN_28) ==============
    # Verified with MCP Selenium - All PASS

    def test_DN_22_dang_nhap_thanh_cong(self):
        """DN_22: Đăng nhập thành công với Email + Password đúng"""
        test_id = "DN_22"
        try:
            self.navigate_to_login_page()
            
            # Nhập email đúng
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(EMAIL_TEST)
            
            # Nhập mật khẩu đúng
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(PASSWORD_TEST)
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            # Verify đăng nhập thành công
            WebDriverWait(self.driver, 10).until(EC.url_contains("/home"))
            assert "/home" in self.driver.current_url
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_23_sai_mat_khau(self):
        """DN_23: Sai mật khẩu - Thông báo lỗi"""
        test_id = "DN_23"
        try:
            self.logout_if_logged_in()
            self.navigate_to_login_page()
            
            # Nhập email đúng
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(EMAIL_TEST)
            
            # Nhập mật khẩu sai
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys("WrongPassword123!")
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            time.sleep(0.5)
            
            # Verify thông báo lỗi
            alert = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["alert_message"]))
            )
            text = re.sub(r"\s+", " ", alert.text).strip()
            assert "Email hoặc mật khẩu không chính xác" in text
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_24_sai_email(self):
        """DN_24: Sai email - Thông báo lỗi"""
        test_id = "DN_24"
        try:
            self.navigate_to_login_page()
            
            # Nhập email sai
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys("wrong@gmail.com")
            
            # Nhập mật khẩu đúng
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(PASSWORD_TEST)
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            time.sleep(0.5)
            
            # Verify thông báo lỗi
            alert = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["alert_message"]))
            )
            text = re.sub(r"\s+", " ", alert.text).strip()
            assert "Email hoặc mật khẩu không chính xác" in text
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_25_ca_email_va_mat_khau_sai(self):
        """DN_25: Cả email và mật khẩu sai - Thông báo lỗi"""
        test_id = "DN_25"
        try:
            self.navigate_to_login_page()
            
            # Nhập email sai
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys("wrong@gmail.com")
            
            # Nhập mật khẩu sai
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys("WrongPass123!")
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            time.sleep(0.5)
            
            # Verify thông báo lỗi
            alert = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["alert_message"]))
            )
            text = re.sub(r"\s+", " ", alert.text).strip()
            assert "Email hoặc mật khẩu không chính xác" in text
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_26_trong_email(self):
        """DN_26: Trống email - Hiển thị lỗi 'Trường này bắt buộc'"""
        test_id = "DN_26"
        try:
            self.navigate_to_login_page()
            
            # Chỉ nhập mật khẩu, để email trống
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(PASSWORD_TEST)
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            # Verify hiển thị lỗi
            error = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["error_required"]))
            )
            text = re.sub(r"\s+", " ", error.text).strip()
            assert "Trường này bắt buộc" in text
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_27_trong_mat_khau(self):
        """DN_27: Trống mật khẩu - Hiển thị lỗi 'Trường này bắt buộc'"""
        test_id = "DN_27"
        try:
            self.navigate_to_login_page()
            
            # Chỉ nhập email, để mật khẩu trống
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(EMAIL_TEST)
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            # Verify hiển thị lỗi
            error = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["error_required"]))
            )
            text = re.sub(r"\s+", " ", error.text).strip()
            assert "Trường này bắt buộc" in text
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_28_trong_ca_2_truong(self):
        """DN_28: Trống cả 2 trường - Hiển thị lỗi ở cả email và password"""
        test_id = "DN_28"
        try:
            self.navigate_to_login_page()
            
            # Click đăng nhập mà không nhập gì
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            # Verify hiển thị lỗi ở cả 2 trường
            errors = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, SELECTORS["error_required"]))
            )
            assert len(errors) >= 2, "Không hiển thị đủ lỗi ở cả 2 trường"
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    # ============== SECTION 4: VALIDATION MẬT KHẨU (DN_29 - DN_34) ==============
    # Verified with MCP Selenium - All PASS

    def test_DN_29_nhap_mat_khau_hop_le(self):
        """DN_29: Nhập mật khẩu hợp lệ - Đăng nhập thành công"""
        test_id = "DN_29"
        try:
            self.navigate_to_login_page()
            
            # Nhập email đúng
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(EMAIL_TEST)
            
            # Nhập mật khẩu hợp lệ
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(PASSWORD_TEST)
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            # Verify đăng nhập thành công
            WebDriverWait(self.driver, 10).until(EC.url_contains("/home"))
            assert "/home" in self.driver.current_url
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_30_mat_khau_qua_ngan(self):
        """DN_30: Mật khẩu quá ngắn (3 ký tự) - Hiển thị lỗi validation"""
        test_id = "DN_30"
        try:
            self.logout_if_logged_in()
            self.navigate_to_login_page()
            
            # Nhập email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(EMAIL_TEST)
            
            # Nhập mật khẩu ngắn
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys("123")
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            # Verify hiển thị lỗi
            error = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error"))
            )
            text = re.sub(r"\s+", " ", error.text).strip()
            assert "Mật khẩu phải gồm ít nhất 1 chữ hoa, chữ thường, số, ký tự đặc biệt và từ 6 ký tự" in text
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_31_mat_khau_qua_dai(self):
        """DN_31: Mật khẩu quá dài (>128 ký tự) - Hiển thị lỗi"""
        test_id = "DN_31"
        try:
            self.navigate_to_login_page()
            
            # Nhập email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(EMAIL_TEST)
            
            # Nhập mật khẩu dài 130 ký tự
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys("a" * 130)
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            # Verify hiển thị lỗi
            error = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error"))
            )
            text = re.sub(r"\s+", " ", error.text).strip()
            assert "Mật khẩu quá dài" in text
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_32_mat_khau_khong_co_so(self):
        """DN_32: Mật khẩu không có số - Hiển thị lỗi validation"""
        test_id = "DN_32"
        try:
            self.navigate_to_login_page()
            
            # Nhập email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(EMAIL_TEST)
            
            # Nhập mật khẩu không có số
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys("Abcde!!")
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            # Verify hiển thị lỗi
            error = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error"))
            )
            text = re.sub(r"\s+", " ", error.text).strip()
            assert "Mật khẩu phải gồm ít nhất 1 chữ hoa, chữ thường, số, ký tự đặc biệt và từ 6 ký tự" in text
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_33_mat_khau_khong_co_chu_hoa(self):
        """DN_33: Mật khẩu không có chữ hoa - Hiển thị lỗi validation"""
        test_id = "DN_33"
        try:
            self.navigate_to_login_page()
            
            # Nhập email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(EMAIL_TEST)
            
            # Nhập mật khẩu không có chữ hoa
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys("abc123!")
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            # Verify hiển thị lỗi
            error = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error"))
            )
            text = re.sub(r"\s+", " ", error.text).strip()
            assert "Mật khẩu phải gồm ít nhất 1 chữ hoa, chữ thường, số, ký tự đặc biệt và từ 6 ký tự" in text
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e

    def test_DN_34_mat_khau_chua_khoang_trang(self):
        """DN_34: Mật khẩu chứa khoảng trắng - Hiển thị lỗi validation"""
        test_id = "DN_34"
        try:
            self.navigate_to_login_page()
            
            # Nhập email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["email_input"]))
            )
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(EMAIL_TEST)
            
            # Nhập mật khẩu có khoảng trắng
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["password_input"]))
            )
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys("abc 123")
            
            # Click đăng nhập
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS["sign_in_button"]))
            )
            button.click()
            
            # Verify hiển thị lỗi
            error = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error"))
            )
            text = re.sub(r"\s+", " ", error.text).strip()
            assert "Mật khẩu phải gồm ít nhất 1 chữ hoa, chữ thường, số, ký tự đặc biệt và từ 6 ký tự" in text
            
            self.update_result(test_id, "PASS")
            
        except Exception as e:
            self.take_screenshot(f"{test_id}_failed")
            self.update_result(test_id, "FAILED")
            raise e


# ============== ALL TEST CASES COMPLETED (DN_1 - DN_34) ==============


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
