import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from config.settings import VALID_USER, VALID_PASSWORD

@pytest.mark.smoke
class TestDangNhap:

    def test_login_page_ui_elements(self, login_page: LoginPage):
        login_page.open()
        time.sleep(1.5)  # Đợi để quan sát UI
        assert login_page.username_field_visible(), "Trường Tên đăng nhập không hiển thị"
        assert login_page.password_field_visible(), "Trường Mật khẩu không hiển thị"
        assert "đăng nhập" in login_page.get_title().lower(), "Tiêu đề trang không đúng"
        assert login_page.forgot_password_link_visible(), "Link Quên mật khẩu không hiển thị"
        time.sleep(1)

    @pytest.mark.smoke
    def test_login_success(self, login_page: LoginPage):
        login_page.open()
        time.sleep(1)

        login_page.enter_username(VALID_USER)
        time.sleep(0.5)

        login_page.enter_password(VALID_PASSWORD)
        time.sleep(1)

        try:
            toggle_eye = login_page.driver.find_element(By.ID, "toggle-icon")
            login_page.driver.execute_script("arguments[0].click();", toggle_eye)
            time.sleep(2)
        except Exception as e:
            print(f"Không thao tác được nút hiện mật khẩu: {e}")

        login_page.click_login()

        WebDriverWait(login_page.driver, 10).until(
            lambda d: "dang-nhap" not in d.current_url
        )
        time.sleep(2)
        assert "dang-nhap" not in login_page.get_current_url()

    def test_login_wrong_password(self, login_page: LoginPage):
        login_page.open()

        login_page.enter_username(VALID_USER)
        login_page.enter_password("WrongPass123@")

        toggle_eye = login_page.driver.find_element(By.ID, "toggle-icon")
        login_page.driver.execute_script("arguments[0].click();", toggle_eye)
        time.sleep(2)

        login_page.click_login()
        time.sleep(1.5)

        assert login_page.error_message_visible()
        assert "dang-nhap" in login_page.get_current_url()

    def test_login_invalid_username(self, login_page: LoginPage):
        login_page.open()
        time.sleep(1)

        login_page.enter_username("nonexistent_user_99")
        time.sleep(0.5)

        login_page.enter_password(VALID_PASSWORD)
        time.sleep(1)
        toggle_eye = login_page.driver.find_element(By.ID, "toggle-icon")
        login_page.driver.execute_script("arguments[0].click();", toggle_eye)
        time.sleep(2)  # Đợi 2s để nhìn rõ mật khẩu trước khi báo lỗi

        login_page.click_login()

        time.sleep(1.5)
        assert login_page.error_message_visible(), "Không báo lỗi khi tài khoản không tồn tại"
        assert "dang-nhap" in login_page.get_current_url()
        time.sleep(1)

    def test_login_empty_username(self, login_page: LoginPage):
        login_page.open()
        time.sleep(1)

        login_page.enter_password(VALID_PASSWORD)
        time.sleep(1)
        toggle_eye = login_page.driver.find_element(By.ID, "toggle-icon")
        login_page.driver.execute_script("arguments[0].click();", toggle_eye)
        time.sleep(2)

        login_page.click_login()
        time.sleep(1)

        assert login_page.username_error_visible(), "Phải báo lỗi khi username trống"
        time.sleep(1)

    def test_login_empty_password(self, login_page: LoginPage):
        login_page.open()
        time.sleep(1)
        login_page.enter_username(VALID_USER)
        time.sleep(0.5)
        login_page.click_login()

        time.sleep(1)
        assert login_page.password_error_visible(), "Phải báo lỗi khi mật khẩu trống"
        time.sleep(1)

    def test_login_empty_both_fields(self, login_page: LoginPage):
        login_page.open()
        time.sleep(1)
        login_page.click_login()

        time.sleep(1.5)
        assert login_page.username_error_visible() or login_page.password_error_visible(), \
            "Phải hiển thị lỗi validate cho cả 2 trường"
        assert "dang-nhap" in login_page.get_current_url()
        time.sleep(1)

    def test_password_toggle_visibility(self, login_page: LoginPage):
        login_page.open()
        time.sleep(1)
        login_page.enter_password(VALID_PASSWORD)
        time.sleep(1)

        pwd_field = login_page.get_password_field_element()
        assert pwd_field.get_attribute("type") == "password"

        login_page.toggle_password_visibility()
        time.sleep(2)
        assert pwd_field.get_attribute("type") == "text"
        time.sleep(1)