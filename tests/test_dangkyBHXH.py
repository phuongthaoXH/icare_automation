import pytest
import time
from selenium.webdriver.common.by import By
from pages.dangkyBHXH_page import DangKyBHXHPage
from config.settings import VALID_USER, VALID_PASSWORD, LOGIN_URL


class TestDangKyBHXH:

    @pytest.fixture(autouse=True)
    def setup_method(self, logged_in_driver):
        self.driver = logged_in_driver
        self.dk_page = DangKyBHXHPage(self.driver)

        self.driver.get("https://test.tokhaibaohiem.vn/thong-tin-don-vi/thong-tin-dang-ky-dich-vu")
        time.sleep(2)

    def test_tc01_cap_nhat_cks_hsm_thanh_cong(self):
        print("\n--- Bắt đầu TC01: Cập nhật CKS HSM ---")

        self.dk_page.click_cap_nhat_cks()

        self.dk_page.click_ky_hsm()

        print("[INFO] Đợi 5 giây để hệ thống xử lý chữ ký...")
        time.sleep(5)

        self.dk_page.click_xac_nhan()
        time.sleep(2)

        self.dk_page.click_tra_cuu()


        print("\n[INFO] Test Case Pass: Cập nhật CKS HSM hoàn tất.")

    def test_tc02_cap_nhat_thong_tin_hsm_thanh_cong(self):
        print("\n--- Bắt đầu TC02: Cập nhật thông tin qua HSM ---")

        self.dk_page.click_cap_nhat_thong_tin()
        time.sleep(2)

        self.dk_page.click_ky_hsm()

        print("[INFO] Đợi 5 giây để hệ thống xử lý chữ ký...")
        time.sleep(5)

        self.dk_page.click_xac_nhan()
        time.sleep(2)

        self.dk_page.click_tra_cuu()

        print("\n[INFO] Test Case TC02 Pass: Cập nhật thông tin HSM hoàn tất.")

    def test_tc03_ngung_su_dung_dv_hsm_thanh_cong(self):
        print("\n--- Bắt đầu TC03: Ngừng sử dụng dịch vụ qua HSM ---")

        self.dk_page.click_ngung_su_dung_dv_ngoai()
        time.sleep(1)

        self.dk_page.nhap_ly_do_ngung("Ngừng dịch vụ test")
        time.sleep(2)

        self.dk_page.click_xac_nhan_ngung_popup()

        self.dk_page.click_ky_hsm()
        time.sleep(5)

        self.dk_page.click_xac_nhan()
        time.sleep(2)

        self.dk_page.click_tra_cuu()

        print("\n[INFO] Test Case TC03 Pass: Đã ngừng dịch vụ và tra cứu xong.")

    def test_tc04_dang_ky_su_dung_hsm_thanh_cong(self):
        print("\n--- Bắt đầu TC04: Đăng ký sử dụng qua HSM ---")

        self.dk_page.click_dang_ky_su_dung()
        time.sleep(1)

        self.dk_page.click_ky_hsm()
        time.sleep(5)

        self.dk_page.click_xac_nhan()
        time.sleep(2)

        self.dk_page.click_tra_cuu()

        print("\n[INFO] Test Case TC04 Pass: Đăng ký sử dụng HSM hoàn tất.")
