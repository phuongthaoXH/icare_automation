import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.dangkyV2_page import DangKyV2Page
import time


class TestDangKyV2(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.implicitly_wait(10)

        self.dang_ky_page = DangKyV2Page(self.driver)

    def test_search_tax_code_success(self):
        self.dang_ky_page.open_page()
        time.sleep(2)

        tax_code_to_test = "0107489961"
        print(f"Đang nhập mã số thuế: {tax_code_to_test}...")
        self.dang_ky_page.enter_tax_code(tax_code_to_test)

        time.sleep(1)

        print("Đang nhấn nút tìm kiếm...")
        self.dang_ky_page.click_search()

        print("Chờ 5 giây để xem kết quả trước khi đóng trình duyệt...")
        time.sleep(5)

        self.dang_ky_page.select_province("Thành phố Hà Nội")
        time.sleep(1)

        self.dang_ky_page.select_district("Phường Hoàn Kiếm")

        time.sleep(5)

        print("Đang chọn Cơ quan BHXH tỉnh...")
        self.dang_ky_page.select_bhxh_province("01 - Thành phố Hà Nội")
        time.sleep(1)

        print("Đang chọn Cơ quan BHXH quản lý...")
        self.dang_ky_page.select_bhxh_management("001 - BHXH thành phố Hà Nội")
        time.sleep(5)

        path_of_file = r"C:\Users\Administrator\OneDrive\Pictures\face.jpg"
        print("Đang thực hiện tải file đính kèm...")
        self.dang_ky_page.upload_file(path_of_file)
        print("Hoàn tất tải file, chờ 5 giây...")
        time.sleep(5)

        print("Đang nhập ghi chú...")
        self.dang_ky_page.enter_note("Đăng ký cấp mã")
        print("Hoàn tất các bước, chờ 5 giây để kiểm tra lại...")
        time.sleep(5)


        self.dang_ky_page.wait_for_captcha_input()
        time.sleep(5)

        self.dang_ky_page.click_final_register()
        self.dang_ky_page.select_sign_easyca()

        print("--- QUY TRÌNH TEST HOÀN TẤT ---")

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()