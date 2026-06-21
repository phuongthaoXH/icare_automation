
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from config.settings import LOGIN_URL, DEFAULT_TIMEOUT

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    _USERNAME_SELECTORS = ["#Input_UserName", "input[name='Input.UserName']", "#username"]
    _PASSWORD_SELECTORS = ["#password-input", "input[name='Input.Password']", "#password"]
    _BTN_LOGIN_SELECTORS = ["button[type='submit']", ".btn-primary"]

    _ERROR_MESSAGE_SELECTOR = ".total-message, .swal2-html-container, .alert-danger, .validation-summary-errors"
    _USER_ERROR_SELECTOR = "#Input_UserName-error, [data-valmsg-for='Input.UserName']"
    _PASS_ERROR_SELECTOR = "#password-input-error, [data-valmsg-for='Input.Password']"

    def open(self):
        logger.info(f"Mở trang đăng nhập: {LOGIN_URL}")
        self.driver.get(LOGIN_URL)

    def enter_username(self, username: str):
        el = self._wait_for_element(By.CSS_SELECTOR, self._USERNAME_SELECTORS[0])
        el.clear()
        el.send_keys(username)
        logger.info(f"Nhập username: {username}")

    def enter_password(self, password: str):
        el = self._wait_for_element(By.CSS_SELECTOR, self._PASSWORD_SELECTORS[0])
        el.clear()
        el.send_keys(password)
        logger.info("Nhập password: ***")

    def click_login(self):
        try:
            el = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self._BTN_LOGIN_SELECTORS[0])))
            el.click()
        except:
            el = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Đăng nhập')]")
            el.click()
        logger.info("Nhấn nút Đăng nhập")

    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()


    def error_message_visible(self) -> bool:
        try:
            el = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self._ERROR_MESSAGE_SELECTOR))
            )
            return el.is_displayed()
        except:
            return False

    def username_error_visible(self) -> bool:
        try:
            el = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self._USER_ERROR_SELECTOR))
            )
            return el.is_displayed()
        except:
            return False

    def password_error_visible(self) -> bool:
        try:
            el = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self._PASS_ERROR_SELECTOR))
            )
            return el.is_displayed()
        except:
            return False

    def username_field_visible(self) -> bool:
        return self.driver.find_element(By.CSS_SELECTOR, self._USERNAME_SELECTORS[0]).is_displayed()

    def password_field_visible(self) -> bool:
        return self.driver.find_element(By.CSS_SELECTOR, self._PASSWORD_SELECTORS[0]).is_displayed()

    def forgot_password_link_visible(self) -> bool:
        try:
            el = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Quên mật khẩu')]")
            return el.is_displayed()
        except:
            return False

    def toggle_password_visibility(self):
        try:
            el = self.driver.find_element(By.ID, "toggle-icon")
            self.driver.execute_script("arguments[0].click();", el)
            logger.info("Đã click toggle hiển thị mật khẩu bằng JS")
        except:
            logger.warning("Không tìm thấy icon mắt")

    def get_password_field_element(self):
        return self.driver.find_element(By.CSS_SELECTOR, self._PASSWORD_SELECTORS[0])

    def get_current_url(self):
        return self.driver.current_url

    def get_title(self):
        return self.driver.title

    def _wait_for_element(self, by, selector, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, selector)))