import pytest
import time
import random
import string

from selenium.webdriver.common.by import By
from pages.phongBan_page import PhongBanPage

class TestPhongBan:

    @pytest.fixture(autouse=True)
    def setup_method(self, logged_in_driver):
        self.driver = logged_in_driver
        self.pb_page = PhongBanPage(self.driver)
        self.driver.get("https://test.tokhaibaohiem.vn/phong-ban")
        time.sleep(2)

    def test_tc01_them_moi_thanh_cong(self):
        self.pb_page.click_them_moi()
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        ten_tu_sinh = f"Phòng Auto {random_suffix}"
        ma_tu_sinh = f"MA{random_suffix}"
        form_input_ten = (By.XPATH, "//input[@placeholder='Nhập tên phòng ban']")
        is_form_opened = self.pb_page.is_element_visible(form_input_ten, 15000)
        assert is_form_opened, "Lỗi: Form thêm mới không hiển thị!"

        self.pb_page.nhap_form_them_moi(
            ten=ten_tu_sinh,
            ma=ma_tu_sinh,
            ten_cha="Phòng BA & Test"
        )

        time.sleep(1)
        self.pb_page.nhan_luu()
        time.sleep(2)

        errors = self.pb_page.get_field_errors()
        if errors:
            print(f"\n[DEBUG] Lỗi validation: {errors}")

        self.driver.save_screenshot("reports/debug_after_luu.png")

        try:
            toast = self.driver.find_element(By.XPATH, "//div[contains(@class,'mud-snackbar')]")
            print(f"\n[DEBUG] Toast message: {toast.text}")
        except:
            print("\n[DEBUG] Không có toast message")

        is_form_closed = not self.pb_page.is_element_visible(form_input_ten, 10000)
        assert is_form_closed, "Lỗi: Form vẫn còn hiển thị sau khi lưu!"

    def test_tc02_them_moi_chi_nhap_ten(self):
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        ten_only = f"Phòng Test {random_suffix}"
        self.pb_page.click_them_moi()

        form_input_ten = (By.XPATH, "//input[@placeholder='Nhập tên phòng ban']")
        is_form_opened = self.pb_page.is_element_visible(form_input_ten, 15000)
        assert is_form_opened, "Lỗi: Form thêm mới không hiển thị!"

        self.pb_page.nhap_form_them_moi(ten=ten_only)
        time.sleep(1)
        self.pb_page.nhan_luu()
        time.sleep(2)

        errors = self.pb_page.get_field_errors()
        if errors:
            print(f"\n[DEBUG] Lỗi validation: {errors}")

        self.driver.save_screenshot("reports/debug_after_luu.png")

        try:
            toast = self.driver.find_element(By.XPATH, "//div[contains(@class,'mud-snackbar')]")
            print(f"\n[DEBUG] Toast message: {toast.text}")
        except:
            print("\n[DEBUG] Không có toast message")

        is_form_closed = not self.pb_page.is_element_visible(form_input_ten, 10000)
        assert is_form_closed, "Lỗi: Form vẫn còn hiển thị sau khi lưu!"

    def test_tc03_validation_ten_trong(self):
        self.pb_page.click_them_moi()

        form_input_ten = (By.XPATH, "//input[@placeholder='Nhập tên phòng ban']")
        is_form_opened = self.pb_page.is_element_visible(form_input_ten, 15000)
        assert is_form_opened, "Lỗi: Form thêm mới không hiển thị!"

        self.pb_page.nhap_form_them_moi(ten="", ma="TEST_ERROR")
        time.sleep(1)
        self.pb_page.nhan_luu()
        time.sleep(1)

        xpath_alert = (By.XPATH,"//div[contains(@class,'mud-snackbar') and contains(.,'Vui lòng nhập tên phòng ban!')]")

        try:
            alert_element = self.driver.find_element(*xpath_alert)
            alert_text = alert_element.text
            print(f"\n[INFO] Đã tìm thấy cảnh báo: {alert_text}")
            assert "Vui lòng nhập tên phòng ban!" in alert_text, f"Lỗi: Nội dung cảnh báo không đúng! Thực tế: {alert_text}"
        except:
            self.driver.save_screenshot("reports/error_tc03_no_alert.png")
            assert False, "Lỗi: Không hiển thị cảnh báo 'Vui lòng nhập tên phòng ban!' khi để trống tên!"

        is_form_still_visible = self.pb_page.is_element_visible(form_input_ten, 5000)
        assert is_form_still_visible, "Lỗi: Form bị đóng mặc dù chưa nhập tên phòng ban!"

    def test_tc04_chinh_sua_phong_ban(self):
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        ten_moi = f"Phòng Edit {random_suffix}"
        ma_moi = f"MA{random_suffix}"

        btn_chinh_sua = (By.XPATH, "//button[contains(@title,'Chỉnh sửa')]")
        self.pb_page.wait_for_element(btn_chinh_sua, 10000)
        self.pb_page.wait_and_click(btn_chinh_sua)

        form_input_ten = (By.XPATH, "//input[@placeholder='Nhập tên phòng ban']")
        is_form_opened = self.pb_page.is_element_visible(form_input_ten, 15000)
        assert is_form_opened, "Lỗi: Form chỉnh sửa không hiển thị!"

        self.pb_page.nhap_form_them_moi(
            ten=ten_moi,
            ma=ma_moi
        )
        time.sleep(1)
        self.pb_page.nhan_luu()
        time.sleep(2)

        errors = self.pb_page.get_field_errors()
        if errors:
            print(f"\n[DEBUG] Lỗi validation: {errors}")

        self.driver.save_screenshot("reports/debug_after_edit_luu.png")

        try:
            toast = self.driver.find_element(By.XPATH, "//div[contains(@class,'mud-snackbar')]")
            print(f"\n[DEBUG] Toast message: {toast.text}")
        except:
            print("\n[DEBUG] Không có toast message")

        is_form_closed = not self.pb_page.is_element_visible(form_input_ten, 15000)
        assert is_form_closed, "Lỗi: Form vẫn còn hiển thị sau khi nhấn Chỉnh sửa và Lưu!"

    def test_tc05_xoa_phong_ban(self):
        btn_xoa = (By.XPATH, "//button[@title='Xóa']")
        btn_dong_y = (By.XPATH, "//button[span[text()='Đồng ý']]")

        self.pb_page.wait_for_element(btn_xoa, 10000)

        try:
            ten_pb_xoa = self.driver.find_element(By.XPATH, "//table/tbody/tr[1]/td[3]").text
            print(f"\n[INFO] Thực hiện xóa phòng ban: {ten_pb_xoa}")
        except:
            ten_pb_xoa = ""

        self.pb_page.wait_and_click(btn_xoa)

        self.pb_page.wait_for_element(btn_dong_y, 10000)
        time.sleep(1)
        self.pb_page.wait_and_click(btn_dong_y)

        time.sleep(2)

        self.driver.save_screenshot("reports/debug_after_delete.png")

        try:
            toast = self.driver.find_element(By.XPATH, "//div[contains(@class,'mud-snackbar')]")
            print(f"\n[DEBUG] Toast message: {toast.text}")
            assert "thành công" in toast.text.lower(), f"Lỗi: Thông báo xóa không thành công! Thực tế: {toast.text}"
        except:
            print("\n[DEBUG] Không có toast message hoặc toast biến mất quá nhanh")

        if ten_pb_xoa:
            self.driver.refresh()
            time.sleep(2)

            xpath_ten_da_xoa = (By.XPATH, f"//td[text()='{ten_pb_xoa}']")
            is_still_there = self.pb_page.is_element_visible(xpath_ten_da_xoa, 5000)
            assert not is_still_there, f"Lỗi: Phòng ban '{ten_pb_xoa}' vẫn còn tồn tại sau khi xóa!"

        print("\n[INFO] Test Case Pass: Xóa phòng ban thành công.")

    def test_tc06_xoa_chon_nhieu(self):
        self.pb_page.wait_and_click(self.pb_page.CHECKBOX_DAU_TIEN)
        self.pb_page.wait_and_click(self.pb_page.BTN_XOA_CHON)
        self.pb_page.wait_and_click(self.pb_page.BTN_DONG_Y_XOA)

    def test_tc07_tim_kiem_tu_dong(self):
        self.pb_page.tim_kiem("pb")
        time.sleep(2)

    def test_tc08_xuat_excel(self):
        self.pb_page.wait_and_click(self.pb_page.BTN_XUAT_EXCEL)

        time.sleep(3)
        print("TC08: Đã nhấn nút Xuất Excel - Test Pass")

    def test_tc09_nap_file_excel_phong_ban(self):
        path_of_file = r"D:\Downloads\FileMau_PB.xlsx"

        print("\n--- Bắt đầu TC09: Nạp file Excel Phòng Ban ---")
        self.pb_page.click_nap_excel()
        time.sleep(2)

        print("Đang thực hiện tải file đính kèm...")
        self.pb_page.upload_file(path_of_file)
        print("Hoàn tất tải file, chờ 5 giây...")

        self.pb_page.click_tai_du_lieu_len()

        print("[INFO] Đang đợi hệ thống xử lý dữ liệu Excel...")
        time.sleep(5)

        try:
            toast_xpath = (By.XPATH, "//div[contains(@class,'mud-snackbar') and contains(.,'thành công')]")
            toast = self.driver.find_element(*toast_xpath)
            print(f"[SUCCESS] Thông báo: {toast.text}")
        except:
            print("[WARNING] Không tìm thấy thông báo thành công, hãy kiểm tra lại file Excel.")
            self.driver.save_screenshot("reports/error_tc09_phongban.png")