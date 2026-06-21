import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys


class TraCuuPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://test.tokhaibaohiem.vn/tra-cuu-dang-ky-lan-dau"

        # Locators - Sử dụng XPath linh hoạt để tránh ID thay đổi
        self.tax_code_input = (By.XPATH, "//input[@placeholder='Nhập mã số thuế']")
        self.search_button = (By.XPATH, "//button[contains(@class, 'mud-input-adornment-icon-button')]")
        self.result_rows = (By.XPATH, "//table//tbody/tr")
        self.snackbar_message = (By.CSS_SELECTOR, "#mud-snackbar-container .mud-snackbar-content-text")
    def open_page(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        # Đợi trang ổn định sau khi load
        time.sleep(3)

    def enter_tax_code_safely(self, tax_code):
        print(f"Bắt đầu nhập MST: {tax_code}")

        for char in tax_code:
            attempt = 0
            while attempt < 3:
                try:
                    wait = WebDriverWait(self.driver, 5)
                    input_el = wait.until(EC.element_to_be_clickable(self.tax_code_input))
                    input_el.send_keys(char)
                    time.sleep(0.1)
                    break
                except StaleElementReferenceException:
                    attempt += 1
                    time.sleep(0.5)
        print("Nhập xong, nghỉ 2s...")
        time.sleep(2)

    def click_search_safely(self):
        """Nhấn nút tra cứu và đợi load"""
        wait = WebDriverWait(self.driver, 10)
        btn = wait.until(EC.element_to_be_clickable(self.search_button))
        btn.click()
        print("Đã nhấn Tra cứu, đợi dữ liệu 2s...")
        time.sleep(2)

    def is_data_found(self):
        try:
            time.sleep(2)
            rows = self.driver.find_elements(*self.result_rows)
            if len(rows) == 0:
                return False
            combined_text = "".join([row.text.lower() for row in rows])
            if "chưa có dữ liệu" in combined_text or "không có dữ liệu" in combined_text:
                print("Hệ thống hiển thị: Chưa có dữ liệu (Đúng kỳ vọng cho TC2)")
                return False

            return True
        except Exception as e:
            print(f"Lỗi khi kiểm tra dữ liệu: {e}")
            return False

    def clear_input(self):
        """Xóa sạch ô nhập MST bằng phím tắt để đảm bảo validate được kích hoạt"""
        wait = WebDriverWait(self.driver, 10)
        input_el = wait.until(EC.element_to_be_clickable(self.tax_code_input))
        input_el.send_keys(Keys.CONTROL + "a")
        input_el.send_keys(Keys.DELETE)
        time.sleep(1)

    def get_snackbar_error_text(self, timeout=5):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "v-snack__content"))
            )

            error_text = element.get_attribute("innerText").strip()

            if not error_text:
                error_text = element.text.strip()

            return error_text
        except:
            return ""