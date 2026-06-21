import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
logger = logging.getLogger(__name__)


class DashboardPage(BasePage):
    _MENU_THU_TUC = "a[href*='thu-tuc'], a.menu-thu-tuc, .nav-link:contains('thủ tục')"
    _USER_INFO = ".navbar-user, .user-menu, [class*='user'], [class*='account']"
    _LOGOUT_BTN = "a[href*='dang-xuat'], .btn-logout, button:contains('Đăng xuất')"

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def is_loaded(self) -> bool:
        return "dang-nhap" not in self.get_url().lower()

    def navigate_to_thu_tuc_600(self) -> bool:
        logger.info("Điều hướng đến Thủ tục 600")
        menu_xpaths = [
            "//a[contains(text(), 'Danh sách thủ tục')]",
            "//span[contains(text(), 'Thủ tục')]",
            "//a[contains(@href, 'danh-sach-thu-tuc')]"
        ]

        menu_clicked = False
        for xpath in menu_xpaths:
            try:
                if self.is_visible_by_xpath(xpath, timeout=3000):
                    self.driver.find_element(By.XPATH, xpath).click()
                    self.wait_for_load()
                    menu_clicked = True
                    break
            except Exception:
                continue

        thu_tuc_600_xpaths = [
            "//a[contains(text(), '600')]",
            "//td[text()='600']",
            "//tr[contains(., '600')]//a",
            "//*[contains(@data-id, '600')]"
        ]

        for xpath in thu_tuc_600_xpaths:
            try:
                if self.is_visible_by_xpath(xpath, timeout=5000):
                    el = self.driver.find_element(By.XPATH, xpath)
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
                    el.click()
                    self.wait_for_load()
                    return True
            except Exception:
                continue

        logger.error("Không tìm thấy mục Thủ tục 600 trên giao diện")
        return False

    def logout(self):
        logger.info("Đăng xuất tài khoản")
        try:
            if not self.is_visible(self._LOGOUT_BTN, timeout=2000):
                self.click(self._USER_INFO)

            self.click(self._LOGOUT_BTN)
            self.wait_for_load()
        except Exception as e:
            logger.warning(f"Lỗi khi logout: {e}")

    def get_logged_in_user(self) -> str:
        try:
            return self.get_text(self._USER_INFO)
        except Exception:
            return ""

    def is_visible_by_xpath(self, xpath: str, timeout: int) -> bool:
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            WebDriverWait(self.driver, timeout / 1000).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            return True
        except TimeoutException:
            return False