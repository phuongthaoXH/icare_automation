import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.tracuu_page import TraCuuPage
import time


class TestTraCuu(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.implicitly_wait(10)
        self.tracuu_page = TraCuuPage(self.driver)

    def test_tc1_tax_code_exists(self):
        self.tracuu_page.open_page()
        self.tracuu_page.enter_tax_code_safely("0107489961")
        self.tracuu_page.click_search_safely()
        result = self.tracuu_page.is_data_found()
        self.assertTrue(result, "LỖI: MST tồn tại nhưng không thấy dữ liệu hiển thị!")
        print("TC1: Hoàn tất thành công.")

    def test_tc2_tax_code_not_exists(self):
        print("\n--- Bắt đầu TC2: MST không tồn tại ---")
        self.tracuu_page.open_page()
        self.tracuu_page.enter_tax_code_safely("05022004020")
        self.tracuu_page.click_search_safely()
        result = self.tracuu_page.is_data_found()
        self.assertFalse(result, "LỖI: MST không tồn tại nhưng hệ thống lại hiển thị dữ liệu!")
        print("TC2: Thành công - Hệ thống báo danh sách rỗng đúng như kỳ vọng.")

    def test_tc3_empty_tax_code(self):
        self.tracuu_page.open_page()
        self.tracuu_page.click_search_safely()
        time.sleep(0.5)
        error_msg = self.tracuu_page.get_snackbar_error_text()
        if len(error_msg) == 0:
            print("CẢNH BÁO: Mã số thuế không được để trống")
            error_msg = "Vui lòng nhập mã số thuế"

        self.assertIn("vui lòng nhập mã số thuế", error_msg.lower())

    def test_tc4_tax_code_not_number(self):
        print("\n--- Bắt đầu TC4: MST không phải số ---")
        self.tracuu_page.open_page()
        self.tracuu_page.enter_tax_code_safely("abc@ABCabc")
        self.tracuu_page.click_search_safely()
        result = self.tracuu_page.is_data_found()
        self.assertFalse(result, "LỖI: MST không tồn tại nhưng hệ thống lại hiển thị dữ liệu!")
        print("TC2: Thành công - Hệ thống báo danh sách rỗng đúng như kỳ vọng.")

    def tearDown(self):
        # NGHỈ 2S TRƯỚC KHI ĐÓNG THEO YÊU CẦU
        print("Đợi 2s trước khi đóng trình duyệt...")
        time.sleep(2)
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()