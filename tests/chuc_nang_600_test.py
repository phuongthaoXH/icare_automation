import pytest
import time
from pages.login_page import LoginPage
from pages.chuc_nang_600_page import ChucNang600Page
from config.settings import VALID_USER, VALID_PASSWORD
from selenium.webdriver.common.by import By

class TestChucNang600:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.login_page = LoginPage(driver)
        self.page_600 = ChucNang600Page(driver)

        self.login_page.open()
        self.login_page.login(VALID_USER, VALID_PASSWORD)
        time.sleep(2)

    def test_tao_dot_600_va_nap_excel(self, driver):
        driver.get("https://test.tokhaibaohiem.vn/ke-khai/thu-tuc/ho-so-dien-tu")
        self.page_600.wait_for_spinner_gone()

        self.page_600.select_thu_tuc_600()
        self.page_600.click_tao_dot_ke_khai()
        self.page_600.wait_for_spinner_gone()
        time.sleep(2)

        self.page_600.click_nap_excel()
        file_path = r"D:\Downloads\600_d02.xlsx"
        self.page_600.upload_excel_file(file_path)
        self.page_600.click_tai_du_lieu_len()
        self.page_600.wait_for_spinner_gone()
        time.sleep(2)

        self.page_600.click_tai_excel()

        self.page_600.click_xem_truoc()
        self.page_600.click_tai_excel_preview()
        time.sleep(2)
        self.page_600.click_tai_xml_preview()
        time.sleep(2)
        self.page_600.click_dong_preview()

        self.page_600.wait_for_spinner_gone()
        time.sleep(1)

        self.page_600.click_ky_gui_ho_so()
        self.page_600.click_ky_hsm()
        time.sleep(15)
        self.page_600.click_tra_cuu_ho_so_button()
        time.sleep(15)
        self.page_600.click_link_tra_cuu_ket_qua()

        print("TC PASSED: Toàn bộ quy trình Ký/Gửi và Tra cứu thành công!")
        time.sleep(3)

    def test_themtu_hsns(self, driver):
        driver.get("https://test.tokhaibaohiem.vn/ke-khai/thu-tuc/ho-so-dien-tu")
        self.page_600.wait_for_spinner_gone()

        self.page_600.select_thu_tuc_600()
        self.page_600.click_tao_dot_ke_khai()
        self.page_600.wait_for_spinner_gone()
        time.sleep(2)

        self.page_600.click_them_tu_hsns()
        self.page_600.search_nhan_vien_hsns("thảo")

        self.page_600.chon_nhieu_nhan_vien_hsns(5)

        self.page_600.wait_for_spinner_gone()

        rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'mud-table-root')]//tr")
        assert len(rows) > 1, "Lỗi: Không có nhân sự nào được thêm vào bảng kê khai."

        print("TC PASSED: Đã thêm thành công 5 nhân sự từ HSNS.")
        time.sleep(2)

    def test_sao_chep_600(self, driver):
        driver.get("https://test.tokhaibaohiem.vn/ke-khai/thu-tuc/ho-so-dien-tu")
        self.page_600.wait_for_spinner_gone()

        self.page_600.select_thu_tuc_600()
        self.page_600.click_tao_dot_ke_khai()
        self.page_600.wait_for_spinner_gone()
        time.sleep(2)

        self.page_600.click_sao_chep_ho_so()

        self.page_600.wait_for_spinner_gone()
        print("TC PASSED: Sao chép hồ sơ thành công.")
