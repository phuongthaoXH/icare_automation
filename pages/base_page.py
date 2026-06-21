import logging
import os
import time
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from config.settings import DEFAULT_TIMEOUT, ELEMENT_TIMEOUT, ACTION_TIMEOUT, SCREENSHOT_DIR

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.timeout = ELEMENT_TIMEOUT / 1000  # Chuyển đổi ms sang giây cho Selenium

    # --- NAVIGATION & LOAD HELPERS ---
    def wait_for_load(self, timeout=DEFAULT_TIMEOUT):
        """Chờ trang web load xong hoàn toàn."""
        t = timeout / 1000
        WebDriverWait(self.driver, t).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def wait_for_spinner_gone(self, timeout=DEFAULT_TIMEOUT):
        """Đợi tất cả các loại spinner và lớp phủ của MudBlazor biến mất."""
        # Danh sách các class thường gây treo giao diện trong MudBlazor
        selectors = [
            ".mud-table-loading-overlay",
            ".mud-loading-indicator",
            ".mud-overlay",
            "//div[contains(@class, 'mud-progress-circular')]"  # Thêm xpath cho vòng tròn quay
        ]
        for sel in selectors:
            try:
                by = By.XPATH if sel.startswith("/") else By.CSS_SELECTOR
                WebDriverWait(self.driver, 2).until(
                    EC.invisibility_of_element_located((by, sel))
                )
            except:
                pass  # Nếu không có spinner thì bỏ qua luôn

    def click_element(self, locator, timeout=None):
        try:
            # Thử click bình thường
            self.wait_and_click(locator, timeout)
        except Exception:
            # Nếu fail (thường do bị che bởi overlay), dùng JS Click để ép click
            logger.warning(f"Click bình thường fail, thử Force Click vào {locator}")
            el = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].click();", el)
    def get_url(self) -> str:
        return self.driver.current_url

    def wait_ms(self, ms: int):
        time.sleep(ms / 1000)

    # --- ELEMENT INTERACTION (Dùng CSS Selector) ---
    def wait_for_visible(self, selector: str, timeout=None) -> WebElement:
        t = timeout / 1000 if timeout else self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )

    def click(self, selector: str, timeout=ELEMENT_TIMEOUT):
        """Click vào element dựa trên CSS Selector."""
        el = self.wait_for_visible(selector, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        el.click()

    # Trong file pages/base_page.py
    def get_field_errors(self):
        """Lấy các tin nhắn lỗi đỏ của MudBlazor iCare."""
        # Tìm tất cả các thẻ có class lỗi của MudBlazor
        locators = [
            "//p[contains(@class, 'mud-input-error')]",
            "//div[contains(@class, 'validation-message')]",
            "//span[contains(@class, 'mud-error-text')]"
        ]
        all_errors = []
        for xpath in locators:
            els = self.driver.find_elements(By.XPATH, xpath)
            all_errors.extend([e.text for e in els if e.text.strip() != ""])
        return list(set(all_errors))  # Xóa trùng lặp

    def wait_and_click(self, locator, timeout=None):
        """Đợi phần tử sẵn sàng và click, dùng JS Click nếu bị che khuất."""
        t = timeout / 1000 if timeout else self.timeout
        self.wait_for_spinner_gone()  # Luôn đợi spinner xong mới click

        try:
            el = WebDriverWait(self.driver, t).until(EC.element_to_be_clickable(locator))
            # Cuộn sao cho phần tử nằm ở giữa màn hình để tránh bị Header/Footer che
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", el)
            time.sleep(0.3)
            el.click()
        except Exception:
            try:
                el = self.driver.find_element(*locator)
                self.driver.execute_script("arguments[0].click();", el)
            except Exception as e:
                logger.error(f"Không thể click vào {locator}: {e}")
                raise

    def send_keys(self, locator: tuple, text: str, timeout=None):
        t = timeout / 1000 if timeout else self.timeout
        try:
            el = WebDriverWait(self.driver, t).until(EC.element_to_be_clickable(locator))
            el.click()

            el.send_keys(Keys.CONTROL + "a")
            el.send_keys(Keys.BACKSPACE)

            el.send_keys(text)

            el.send_keys(Keys.TAB)
            time.sleep(0.2)
        except Exception as e:
            logger.error(f"Lỗi nhập liệu vào {locator}: {e}")
            raise



    def wait_for_element(self, locator, timeout=None) -> WebElement:
        t = timeout / 1000 if timeout else self.timeout
        return WebDriverWait(self.driver, t).until(EC.presence_of_element_located(locator))

    def is_element_visible(self, locator, timeout=None) -> bool:
        """Kiểm tra element có hiển thị hay không dựa trên locator (By.XPATH, '...')."""
        t = timeout / 1000 if timeout else (ACTION_TIMEOUT / 1000)
        try:
            WebDriverWait(self.driver, t).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False