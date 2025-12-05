"""
Test Cases cho chức năng Đăng nhập (DN)
"""
import pytest
import re 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

import os
import sys
import time
from datetime import datetime


base = os.getcwd()
path = os.path.dirname(base)
sys.path.append(path)

from gg_sheet.index import ConnectGoogleSheet

from utils.index import update_status_result_to_sheet

from constant.index import LOGIN_TEST_CASE, JSON_NAME, SPREEDSHEET_ID


RUN_INDEX = int(os.environ.get("RUN_INDEX", 1)) # index of round (number of iteration)

class TestLogin:
    driver = None
    start_row = 4
    EMAIL_TEST = "lovecatdat@gmail.com"
    PASSWORD_TEST="123456@Dat"
    


    @classmethod
    def setup_class(cls):
        """Chạy một lần khi bắt đầu tất cả test cases"""
        cls.driver = webdriver.Chrome()
       
        # Load data from Google Sheet
        cls.gg_sheet = ConnectGoogleSheet(JSON_NAME)
        cls.worksheet = cls.gg_sheet.loadSheet_WorkSheet(
            SPREEDSHEET_ID,
            LOGIN_TEST_CASE
        )

        cls.input_test_cases = cls.worksheet.col_values(3)# input for test cases 


        cls.test_failures_dir = "test_failures"
        os.makedirs(cls.test_failures_dir, exist_ok=True)


    @classmethod
    def teardown_class(cls):
        """Chạy sau khi tất cả test cases hoàn thành"""
        if hasattr(cls, 'driver'):
            cls.driver.quit()

    def take_screenshot(self, name):
        """Chụp màn hình và lưu với timestamp"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.test_failures_dir}/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"Screenshot saved: {filename}")
        return filename

    def test_DN_1_kiem_tra_tieu_de_man_hinh(self):
        """DN_1: Test screen title"""
        try:
            self.driver.get("http://14.225.44.169:3000/home")
            self.driver.maximize_window()

            login_button = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-y9vvym-MuiButtonBase-root-MuiButton-root"))
            )
            login_button.click()


            title = title = WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//*[@class='MuiTypography-root MuiTypography-h5 css-1000all-MuiTypography-root']")
                    )
                )

            assert title.is_displayed(), "The 'login' title is not displayed"
            assert title.text == "Đăng nhập"

           
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row += 1
            

        except Exception as e:
            self.take_screenshot("DN_1_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            raise e
    
    def test_DN_2_kiem_tra_label_email(self):
        """DN_2: Kiểm tra label Email"""
        try:

            label = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormLabel-root.MuiInputLabel-root.MuiInputLabel-formControl.MuiInputLabel-animated.MuiInputLabel-shrink")))
            label_email = label[0]

            text = re.sub(r"\s+", " ", label_email.text).strip()

            assert text == "Email *"

            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row += 1
        except Exception as e:
            self.take_screenshot("DN_2_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            raise e
    
    def test_DN_3_kiem_tra_label_mat_khau(self):
        """DN_3: Kiểm tra label Mật khẩu"""
        try:
            

            label = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormLabel-root.MuiInputLabel-root.MuiInputLabel-formControl.MuiInputLabel-animated.MuiInputLabel-shrink")))
            label_password = label[1]

            text = re.sub(r"\s+", " ", label_password.text).strip()
            assert text == "Mật khẩu *"

            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)

            TestLogin.start_row += 1
        except Exception as e:
            self.take_screenshot("DN_3_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            raise e
    
    def test_DN_4_kiem_tra_placeholder_email(self):
        """DN_4: Kiểm tra placeholder Email"""
        try:
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))

            assert email_input.get_attribute("placeholder") == "Nhập email"
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
        except Exception as e:
            self.take_screenshot("DN_4_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_5_kiem_tra_placeholder_password(self):
        """DN_5: Kiểm tra placeholder Password"""
        try:

            password_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))

            assert password_input.get_attribute("placeholder") == "Nhập mật khẩu"
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
        except Exception as e:
            self.take_screenshot("DN_5_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_6_kiem_tra_checkbox_nho_mat_khau(self):
        """DN_6: Kiểm tra checkbox Nhớ mật khẩu"""
        try:
            
            checkbox = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".PrivateSwitchBase-input")
                )
            )


            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_6_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_7_kiem_tra_link_quen_mat_khau(self):
        """DN_7: Kiểm tra link Quên mật khẩu"""
        try:
            link = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Quên mật khẩu?")))
            assert link.is_displayed(), "Link Quên mật khẩu không hiển thị"
            assert link.is_enabled(), "Link không thể click"

            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_7_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_8_kiem_tra_nut_sign_in(self):
        """DN_8: Kiểm tra nút Sign In"""
        try:
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            assert button.is_displayed(), "Nút Sign In không hiển thị"
            bg_color = button.value_of_css_property("background-color")
            text_color = button.value_of_css_property("color")
            border_radius = button.value_of_css_property("border-radius")

            assert "rgba(115, 103, 240, 1)" == bg_color, "Sai màu nền"
            assert "rgba(255, 255, 255, 1)" == text_color, "Sai màu chữ"
            assert "10px" == border_radius, "Sai bo góc"
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_8_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_9_kiem_tra_link_dang_ky(self):
        """DN_9: Kiểm tra link Đăng ký"""
        try:
            link = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Đăng ký")))
            assert link.is_displayed() and link.is_enabled()
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_9_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_10_kiem_tra_icon_facebook(self):
        """DN_10: Kiểm tra icon đăng nhập bằng Facebook"""
        try:
            icon = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-z70jni-MuiButtonBase-root-MuiIconButton-root")))

            assert icon.is_displayed(), "Icon Facebook không hiển thị"

            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_10_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_11_kiem_tra_icon_google(self):
        """DN_11: Kiểm tra icon đăng nhập bằng Google"""
        try:
            icon = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-7qi38e-MuiButtonBase-root-MuiIconButton-root")))
            assert icon.is_displayed(), "Icon Google không hiển thị"

            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_11_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    # # 2. CHỨC NĂNG ĐĂNG NHẬP - TRƯỜNG EMAIL
    
    def test_DN_12_nhap_email_hop_le(self):
        TestLogin.start_row = 17
        """DN_12: Nhập email hợp lệ"""
        try:
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.clear()
            email_input.send_keys(self.input_test_cases[self.start_row - 1].split(":")[1].strip())

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.clear()
            pass_input.send_keys(self.PASSWORD_TEST)

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()

            WebDriverWait(self.driver, 10).until(EC.url_contains("/home"))
            assert "/home" in self.driver.current_url
            
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_12_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_13_nhap_email_thieu_at(self):
        """DN_13: Nhập email không hợp lệ (thiếu @)"""
        try:
            # logout account 
            user_btn = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiAvatar-root.MuiAvatar-circular.MuiAvatar-colorDefault.css-1j1wjvp-MuiAvatar-root")))
            user_btn.click()
          

            logout_btn = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiMenuItem-root.MuiMenuItem-gutters.MuiMenuItem-root.MuiMenuItem-gutters.css-wr5qfr-MuiButtonBase-root-MuiMenuItem-root")))[-1]
            logout_btn.click()


            login_button = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-y9vvym-MuiButtonBase-root-MuiButton-root"))
            )

            login_button.click()

            
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(self.input_test_cases[self.start_row - 1].split(":")[1].strip())

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))

            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(self.PASSWORD_TEST)

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()
            
            error = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error.MuiFormHelperText-sizeSmall.MuiFormHelperText-contained.MuiFormHelperText-filled.Mui-required.css-brfce9-MuiFormHelperText-root")))
            
            text = re.sub(r"\s+", " ", error.text).strip()
            assert "Email không hợp lệ" in text

            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_13_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_14_nhap_email_khong_co_domain(self):
        """DN_14: Nhập email không hợp lệ (không có domain)"""
        try:
         
            
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(self.input_test_cases[self.start_row - 1].split(":")[1].strip())

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(self.PASSWORD_TEST)

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()
            
            error = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error.MuiFormHelperText-sizeSmall.MuiFormHelperText-contained.MuiFormHelperText-filled.Mui-required.css-brfce9-MuiFormHelperText-root")))
            
            text = re.sub(r"\s+", " ", error.text).strip()
            assert "Email không hợp lệ" in text
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_14_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_15_nhap_email_ky_tu_dac_biet_sai(self):
        """DN_15: Nhập email chứa ký tự đặc biệt sai"""
        try:
         
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(self.input_test_cases[self.start_row - 1].split(":")[1].strip())

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(self.PASSWORD_TEST)

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()
            
            error = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error.MuiFormHelperText-sizeSmall.MuiFormHelperText-contained.MuiFormHelperText-filled.Mui-required.css-brfce9-MuiFormHelperText-root")))
            
            text = re.sub(r"\s+", " ", error.text).strip()
            assert "Email không hợp lệ" in text
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_15_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_16_kiem_tra_do_dai_email_max(self):
        """DN_16: Kiểm tra độ dài email max"""

        try:
         
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys("exampl" + "e" * 256 + "@gmail.com")

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(self.PASSWORD_TEST)

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()
            
            error = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error.MuiFormHelperText-sizeSmall.MuiFormHelperText-contained.MuiFormHelperText-filled.Mui-required.css-brfce9-MuiFormHelperText-root")))
            
            text = re.sub(r"\s+", " ", error.text).strip()
            assert "Email vượt quá kí tự cho phép" in text
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_16_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    # # TRƯỜNG MẬT KHẨU
    
    # def test_DN_18_tick_nho_mat_khau(self):
    #     """DN_18: Tick Nhớ mật khẩu → Login"""
    #     try:
    #         self.driver.find_element(By.ID, "email").send_keys("lovecatdat@gmail.com")
    #         self.driver.find_element(By.ID, "password").send_keys("Abc@1234")
    #         self.driver.find_element(By.ID, "remember").click()
    #         self.take_screenshot("DN_18_before_submit")
    #         self.driver.find_element(By.XPATH, "//button[contains(text(),'Sign In')]").click()
            
    #         # Đóng trình duyệt và mở lại
    #         self.driver.quit()
    #         self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #         self.driver.get(self.BASE_URL)
            
    #         # Kiểm tra email được tự động điền
    #         email_value = self.driver.find_element(By.ID, "email").get_attribute("value")
    #         assert email_value == "lovecatdat@gmail.com"
    #         self.take_screenshot("DN_18_success")
    #     except Exception as e:
    #         self.take_screenshot("DN_18_failed")
    #         raise e
    
    # def test_DN_19_tat_nho_mat_khau(self):
    #     """DN_19: Tắt Nhớ mật khẩu"""
    #     try:
    #         self.driver.find_element(By.ID, "email").send_keys("lovecatdat@gmail.com")
    #         self.driver.find_element(By.ID, "password").send_keys("Abc@1234")
    #         self.take_screenshot("DN_19_before_submit")
    #         self.driver.find_element(By.XPATH, "//button[contains(text(),'Sign In')]").click()
            
    #         # Đóng và mở lại
    #         self.driver.quit()
    #         self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #         self.driver.get(self.BASE_URL)
            
    #         email_value = self.driver.find_element(By.ID, "email").get_attribute("value")
    #         assert email_value == ""
    #         self.take_screenshot("DN_19_success")
    #     except Exception as e:
    #         self.take_screenshot("DN_19_failed")
    #         raise e
    
    def test_DN_20_hien_mat_khau(self):
        """DN_20: Hiện mật khẩu"""
        TestLogin.start_row = 26
        try:
         
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys("example@gmail.com")

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(self.PASSWORD_TEST)

            showHiddenIcon = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-edgeEnd.MuiIconButton-sizeMedium.css-xubj68-MuiButtonBase-root-MuiIconButton-root")))
            showHiddenIcon.click()

            assert pass_input.get_attribute("type") == "text"

            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_20_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_21_an_mat_khau(self):
        """DN_21: Ẩn mật khẩu"""
        try:
         
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys("example@gmail.com")

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(self.PASSWORD_TEST)

            showHiddenIcon = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-edgeEnd.MuiIconButton-sizeMedium.css-xubj68-MuiButtonBase-root-MuiIconButton-root")))
            showHiddenIcon.click()

            assert pass_input.get_attribute("type") == "password"

            

            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_21_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    # # BUTTON ĐĂNG NHẬP
    
    def test_DN_22_dang_nhap_thanh_cong(self):
        """DN_22: Đăng nhập thành công"""
        TestLogin.start_row = 29
        try:
         
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(self.EMAIL_TEST)

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(self.PASSWORD_TEST)

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()

            WebDriverWait(self.driver, 10).until(EC.url_contains("/home"))
            assert "/home" in self.driver.current_url
            
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_22_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_23_sai_mat_khau(self):
        try:
            time.sleep(2)
            # logout account 
            user_btn = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiAvatar-root.MuiAvatar-circular.MuiAvatar-colorDefault.css-1j1wjvp-MuiAvatar-root")))
            user_btn.click()
          

            logout_btn = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiMenuItem-root.MuiMenuItem-gutters.MuiMenuItem-root.MuiMenuItem-gutters.css-wr5qfr-MuiButtonBase-root-MuiMenuItem-root")))[-1]
            logout_btn.click()

            login_button = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-y9vvym-MuiButtonBase-root-MuiButton-root"))
            )

            login_button.click()

         
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(self.EMAIL_TEST)

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys("123456@Wrong_password")

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()

            time.sleep(0.5)

            alert_message = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".go4109123758")))
            
            text = re.sub(r"\s+", " ", alert_message.text).strip()
            assert "Email hoặc mật khẩu không chính xác" in text
            
            
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
        except Exception as e:
            self.take_screenshot("DN_23_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_24_sai_email(self):
        """DN_24: Sai email"""
        try:
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys("example@gmail.com")

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(self.PASSWORD_TEST)

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()

            time.sleep(0.5)

            alert_message = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".go4109123758")))
            
            text = re.sub(r"\s+", " ", alert_message.text).strip()
            assert "Email hoặc mật khẩu không chính xác" in text
            
            
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
        except Exception as e:
            self.take_screenshot("DN_24_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_25_ca_email_va_mat_khau_sai(self):
        try:
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys("example@gmail.com")

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys("123456@Wrong_password")

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()

            time.sleep(0.5)

            alert_message = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".go4109123758")))
            
            text = re.sub(r"\s+", " ", alert_message.text).strip()
            assert "Email hoặc mật khẩu không chính xác" in text
            
            
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
        except Exception as e:
            self.take_screenshot("DN_25_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
        
    def test_DN_26_trong_email(self):
        """DN_26: Trống email"""
        try:
         
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(self.PASSWORD_TEST)

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()

            time.sleep(0.5)
            
            error = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error.MuiFormHelperText-sizeSmall.MuiFormHelperText-contained.Mui-required.css-brfce9-MuiFormHelperText-root")))[0]
            
            text = re.sub(r"\s+", " ", error.text).strip()
            assert "Trường này bắt buộc" in text
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_26_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_27_trong_mat_khau(self):
        """DN_27: Trống mật khẩu"""
        try:
         
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(self.EMAIL_TEST)

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()
            
            error_password = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error.MuiFormHelperText-sizeSmall.MuiFormHelperText-contained.Mui-required.css-brfce9-MuiFormHelperText-root")))
            
            text = re.sub(r"\s+", " ", error_password.text).strip()
            assert "Trường này bắt buộc" in text
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_27_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_28_trong_ca_2_truong(self):
        """DN_28: Trống cả 2 trường"""
        try:
         
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()
            
            error_password = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error.MuiFormHelperText-sizeSmall.MuiFormHelperText-contained.Mui-required.css-brfce9-MuiFormHelperText-root")))[1]
            error_email = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error.MuiFormHelperText-sizeSmall.MuiFormHelperText-contained.Mui-required.css-brfce9-MuiFormHelperText-root")))[0]
            
            
            
            text_email = re.sub(r"\s+", " ", error_email.text).strip()
            text_password = re.sub(r"\s+", " ", error_password.text).strip()

            assert "Trường này bắt buộc" in text_email
            assert "Trường này bắt buộc" in text_password
            
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_28_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    
    def test_DN_29_nhap_mat_khau_hop_le(self):
        """DN_29: Nhập mật khẩu hợp lệ"""
        try:
         
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(self.EMAIL_TEST)

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(self.PASSWORD_TEST)

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()
            

            WebDriverWait(self.driver, 10).until(EC.url_contains("/home"))
            assert "/home" in self.driver.current_url           
            
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1

        except Exception as e:
            self.take_screenshot("DN_29_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    
    def test_DN_30_mat_khau_qua_ngan(self):
        """DN_30: Mật khẩu quá ngắn"""
        try:
            time.sleep(2)
            # logout account 
            user_btn = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiAvatar-root.MuiAvatar-circular.MuiAvatar-colorDefault.css-1j1wjvp-MuiAvatar-root")))
            user_btn.click()
          

            logout_btn = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiMenuItem-root.MuiMenuItem-gutters.MuiMenuItem-root.MuiMenuItem-gutters.css-wr5qfr-MuiButtonBase-root-MuiMenuItem-root")))[-1]
            logout_btn.click()

            login_button = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-y9vvym-MuiButtonBase-root-MuiButton-root"))
            )

            login_button.click()

         
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(self.EMAIL_TEST)

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys("123")

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()

            time.sleep(0.5)

            error_password = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error.MuiFormHelperText-sizeSmall.MuiFormHelperText-contained.Mui-required.css-brfce9-MuiFormHelperText-root")))[0]
            
            text = re.sub(r"\s+", " ", error_password.text).strip()
            assert "Mật khẩu phải gồm ít nhất 1 chữ hoa, chữ thường, số, ký tự đặc biệt và từ 6 ký tự" in text
            
            
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
        except Exception as e:
            self.take_screenshot("DN_30_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_31_mat_khau_qua_dai(self):
        """DN_31: Mật khẩu quá dài"""
        try:
            time.sleep(2)

         
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(self.EMAIL_TEST)

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys("a" * 130)

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()

            time.sleep(0.5)

            error_password = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error.MuiFormHelperText-sizeSmall.MuiFormHelperText-contained.Mui-required.css-brfce9-MuiFormHelperText-root")))[0]
            
            text = re.sub(r"\s+", " ", error_password.text).strip()
            assert "Mật khẩu quá dài" in text
            
            
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
        except Exception as e:
            self.take_screenshot("DN_31_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_32_mat_khau_khong_co_so(self):
        """DN_32: Mật khẩu không có số"""
        try:

         
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(self.EMAIL_TEST)

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(self.input_test_cases[self.start_row])

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()

            time.sleep(0.5)

            error_password = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error.MuiFormHelperText-sizeSmall.MuiFormHelperText-contained.Mui-required.css-brfce9-MuiFormHelperText-root")))[0]
            
            text = re.sub(r"\s+", " ", error_password.text).strip()
            assert "Mật khẩu phải gồm ít nhất 1 chữ hoa, chữ thường, số, ký tự đặc biệt và từ 6 ký tự" in text
            
            
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
        except Exception as e:
            self.take_screenshot("DN_30_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_33_mat_khau_khong_co_chu_hoa(self):
        """DN_33: Mật khẩu không có chữ hoa"""
        try:

         
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(self.EMAIL_TEST)

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)
            pass_input.send_keys(self.input_test_cases[self.start_row])

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()

            time.sleep(0.5)

            error_password = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error.MuiFormHelperText-sizeSmall.MuiFormHelperText-contained.Mui-required.css-brfce9-MuiFormHelperText-root")))[0]
            
            text = re.sub(r"\s+", " ", error_password.text).strip()
            assert "Mật khẩu phải gồm ít nhất 1 chữ hoa, chữ thường, số, ký tự đặc biệt và từ 6 ký tự" in text
            
            
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
        except Exception as e:
            self.take_screenshot("DN_30_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e
    
    def test_DN_34_mat_khau_chua_khoang_trang(self):
        """DN_34: Mật khẩu chứa khoảng trắng"""
        try:
           
         
            email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.css-8wyvbo-MuiInputBase-input-MuiFilledInput-input")))
            email_input.click()
            email_input.send_keys(Keys.CONTROL, "a")
            email_input.send_keys(Keys.BACKSPACE)
            email_input.send_keys(self.EMAIL_TEST)

            pass_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputSizeSmall.MuiInputBase-inputAdornedEnd.css-13scjpl-MuiInputBase-input-MuiFilledInput-input")))
            pass_input.click()
            pass_input.send_keys(Keys.CONTROL, "a")
            pass_input.send_keys(Keys.BACKSPACE)

            pass_input.send_keys(self.input_test_cases[self.start_row - 1])
            

            # Button signin
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium")))
            button.click()

            time.sleep(0.5)

            error_password = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error.MuiFormHelperText-sizeSmall.MuiFormHelperText-contained.Mui-required.css-brfce9-MuiFormHelperText-root")))[0]
            
            text = re.sub(r"\s+", " ", error_password.text).strip()
            assert "Mật khẩu phải gồm ít nhất 1 chữ hoa, chữ thường, số, ký tự đặc biệt và từ 6 ký tự" in text
            
            
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["PASS"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
        except Exception as e:
            self.take_screenshot("DN_30_failed")
            update_status_result_to_sheet(worksheet=self.worksheet,base_col="F",row=self.start_row, value_update= ["FAILED"], run_index=RUN_INDEX)
            TestLogin.start_row +=1
            raise e

