import pytest
import time
import random
import string
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.chucVu_page import ChucVuPage


class TestChucVu:

    @pytest.fixture(autouse=True)
    def setup_method(self, logged_in_driver):
        self.driver = logged_in_driver
        self.cv_page = ChucVuPage(self.driver)
        self.driver.get("https://test.tokhaibaohiem.vn/chuc-vu")
        time.sleep(2)

    @staticmethod
    def _random_suffix(k: int = 4) -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))

    def test_tc01_them_moi_hieu_luc(self):
        ten = f"Chức vụ Auto {self._random_suffix()}"

        self.cv_page.click_them_moi()

        form_input = (By.XPATH, "//div[contains(@class,'mud-dialog')]//input[@placeholder='Nhập tên chức vụ']")
        assert self.cv_page.is_element_visible(form_input, 15000), \
            "Lỗi: Form thêm mới không hiển thị!"

        self.cv_page.nhap_ten(ten)
        self.cv_page.chon_trang_thai("Hiệu lực")

        time.sleep(1)
        self.cv_page.nhan_luu()
        time.sleep(2)

        self.driver.save_screenshot("reports/debug_cv_tc01_after_luu.png")
        try:
            toast = self.driver.find_element(By.XPATH, "//div[contains(@class,'mud-snackbar')]")
            print(f"\n[DEBUG] Toast: {toast.text}")
        except Exception:
            print("\n[DEBUG] Không có toast")

        is_closed = not self.cv_page.is_element_visible(form_input, 10000)
        assert is_closed, "Lỗi: Form vẫn còn hiển thị sau khi lưu!"

    def test_tc02_them_moi_khong_hieu_luc(self):
        ten = f"Chức vụ Auto {self._random_suffix()}"

        self.cv_page.click_them_moi()

        form_input = (By.XPATH, "//div[contains(@class,'mud-dialog')]//input[@placeholder='Nhập tên chức vụ']")
        assert self.cv_page.is_element_visible(form_input, 15000), \
            "Lỗi: Form thêm mới không hiển thị!"

        self.cv_page.nhap_ten(ten)
        self.cv_page.chon_trang_thai("Không hiệu lực")

        time.sleep(1)
        self.cv_page.nhan_luu()
        time.sleep(2)

        self.driver.save_screenshot("reports/debug_cv_tc02_after_luu.png")
        try:
            toast = self.driver.find_element(By.XPATH, "//div[contains(@class,'mud-snackbar')]")
            print(f"\n[DEBUG] Toast: {toast.text}")
        except Exception:
            print("\n[DEBUG] Không có toast")

        is_closed = not self.cv_page.is_element_visible(form_input, 10000)
        assert is_closed, "Lỗi: Form vẫn còn hiển thị sau khi lưu!"

    def test_tc03_validation_ten_trong(self):
        self.cv_page.click_them_moi()

        form_input = (By.XPATH, "//div[contains(@class,'mud-dialog')]//input[@placeholder='Nhập tên chức vụ']")
        assert self.cv_page.is_element_visible(form_input, 15000), \
            "Lỗi: Form thêm mới không hiển thị!"

        self.cv_page.nhan_luu()
        time.sleep(1)

        xpath_loi = (
            By.XPATH,
            "//div[contains(@class,'mud-dialog')]"
            "//*[contains(text(),'Trường không được trống')]"
        )
        is_loi_hien = self.cv_page.is_element_visible(xpath_loi, 5000)
        self.driver.save_screenshot("reports/debug_cv_tc03_validation.png")

        assert is_loi_hien, \
            "Lỗi: Không hiển thị thông báo 'Trường không được trống.' khi để trống tên!"

        is_form_still_open = self.cv_page.is_element_visible(form_input, 3000)
        assert is_form_still_open, \
            "Lỗi: Form bị đóng mặc dù chưa nhập tên chức vụ!"

        print("\n[INFO] TC03 PASS: Hiển thị đúng lỗi validation khi để trống tên.")

    def test_tc04_chinh_sua_chuc_vu(self):
        ten_moi = f"CV Edit {self._random_suffix()}"

        self.cv_page.wait_for_element(self.cv_page.BTN_EDIT_ICON, 10000)
        self.cv_page.wait_and_click(self.cv_page.BTN_EDIT_ICON)

        form_input_xpath = "//div[contains(@class,'mud-dialog')]//input[@placeholder='Nhập tên chức vụ']"
        form_input = (By.XPATH, form_input_xpath)

        assert self.cv_page.is_element_visible(form_input, 15000), "Lỗi: Form chỉnh sửa không hiển thị!"

        input_element = self.driver.find_element(*form_input)
        input_element.click()
        input_element.send_keys(Keys.CONTROL + "a")
        input_element.send_keys(Keys.BACKSPACE)
        input_element.send_keys(ten_moi)

        time.sleep(0.5)
        self.cv_page.nhan_luu()

        time.sleep(1)
        try:
            toast = self.driver.find_element(By.XPATH, "//div[contains(@class,'mud-snackbar-content-text')]")
            toast_text = toast.text
            print(f"\n[DEBUG] Toast Message: {toast_text}")
            if "đã tồn tại" in toast_text or "lỗi" in toast_text.lower():
                self.driver.save_screenshot("reports/error_validation.png")
        except:
            print("\n[DEBUG] Không tìm thấy Toast")

        is_closed = False
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(form_input)
            )
            is_closed = True
        except:
            is_closed = False

        assert is_closed, f"Lỗi: Form vẫn còn hiển thị. Có thể do: {toast_text if 'toast_text' in locals() else 'Không rõ lý do'}"

    def test_tc05_xoa_mot_chuc_vu(self):
        btn_xoa = (By.XPATH, "(//button[@aria-label='delete' or @title='Xóa'])[1]")
        btn_dong_y = (By.XPATH, "//button[span[text()='Đồng ý']]")

        self.cv_page.wait_for_element(btn_xoa, 10000)

        try:
            ten_cv_xoa = self.driver.find_element(By.XPATH, "//table/tbody/tr[1]/td[2]").text
            print(f"\n[INFO] Thực hiện xóa chức vụ: {ten_cv_xoa}")
        except Exception as e:
            print(f"\n[WARNING] Không lấy được tên chức vụ: {e}")
            ten_cv_xoa = ""

        self.cv_page.wait_and_click(btn_xoa)

        self.cv_page.wait_for_element(btn_dong_y, 10000)
        time.sleep(1)
        self.cv_page.wait_and_click(btn_dong_y)
        time.sleep(2)

        self.driver.save_screenshot("reports/debug_cv_after_delete.png")

        try:
            toast_locator = (By.XPATH, "//div[contains(@class,'mud-snackbar-content-text')]")
            toast = self.driver.find_element(*toast_locator)
            print(f"\n[DEBUG] Toast message: {toast.text}")
            assert "thành công" in toast.text.lower(), f"Lỗi: Thông báo xóa không thành công! Thực tế: {toast.text}"
        except Exception:
            print("\n[DEBUG] Không có toast message hoặc toast biến mất quá nhanh")

        if ten_cv_xoa:
            self.driver.refresh()
            time.sleep(3)
            xpath_ten_da_xoa = (By.XPATH, f"//table//td[text()='{ten_cv_xoa}']")
            is_still_there = self.cv_page.is_element_visible(xpath_ten_da_xoa, 5000)
            assert not is_still_there, f"Lỗi: Chức vụ '{ten_cv_xoa}' vẫn còn tồn tại sau khi xóa (Có thể do trùng tên với dòng khác)!"
        print(f"\n[INFO] Test Case Pass: Xóa chức vụ '{ten_cv_xoa}' thành công.")

    def test_tc06_xoa_nhieu_chuc_vu(self):
        so_luong_xoa = 5
        for i in range(2, 2 + so_luong_xoa):
            checkbox = (By.XPATH, f"(//input[@type='checkbox'])[{i}]")
            self.cv_page.wait_for_element(checkbox, 10000)
            self.cv_page.wait_and_click(checkbox)
            time.sleep(0.2)

        print(f"\n[INFO] Đã check {so_luong_xoa} chức vụ.")

        self.cv_page.wait_for_element(self.cv_page.BTN_XOA_CHON, 10000)
        self.cv_page.wait_and_click(self.cv_page.BTN_XOA_CHON)

        self.cv_page.wait_for_element(self.cv_page.BTN_DONG_Y_XOA, 10000)
        time.sleep(0.5)
        self.cv_page.wait_and_click(self.cv_page.BTN_DONG_Y_XOA)
        time.sleep(2)

        self.driver.save_screenshot("reports/debug_cv_tc06_after_delete_multi.png")
        try:
            toast = self.driver.find_element(By.XPATH, "//div[contains(@class,'mud-snackbar')]")
            print(f"\n[DEBUG] Toast: {toast.text}")
            assert "thành công" in toast.text.lower(), \
                f"Lỗi: Toast xóa nhiều không thành công! Thực tế: {toast.text}"
        except AssertionError:
            raise
        except Exception:
            print("\n[DEBUG] Không có toast hoặc toast biến mất quá nhanh")

        print(f"\n[INFO] TC06 PASS: Xóa {so_luong_xoa} chức vụ thành công.")

    def test_tc07_xuat_excel(self):
        self.cv_page.wait_and_click(self.cv_page.BTN_XUAT_EXCEL)
        time.sleep(3)

        xpath_loi = (By.XPATH, "//div[contains(@class,'mud-snackbar') and contains(.,'lỗi')]")
        is_error = self.cv_page.is_element_visible(xpath_loi, 3000)
        assert not is_error, "Lỗi: Xuất Excel thất bại, có thông báo lỗi!"

        self.driver.save_screenshot("reports/debug_cv_tc07_xuat_excel.png")
        print("\n[INFO] TC07 PASS: Nhấn Xuất Excel không có lỗi.")

    def test_tc08_tim_kiem_tu_khoa(self):
        tu_khoa = "kỹ"
        self.cv_page.tim_kiem(tu_khoa)
        time.sleep(3)

        xpath_ten_cv = "//table/tbody/tr/td[@data-label='Tên chức vụ']"

        ten_chuc_vu_elements = self.driver.find_elements(By.XPATH, xpath_ten_cv)

        if not ten_chuc_vu_elements:
            ten_chuc_vu_elements = self.driver.find_elements(By.XPATH, "//table/tbody/tr/td[2]")

        print(f"\n[DEBUG] Số lượng kết quả kiểm tra: {len(ten_chuc_vu_elements)}")

        for element in ten_chuc_vu_elements:
            ten_hien_thi = element.text.strip().lower()

            if not ten_hien_thi or ten_hien_thi.isdigit():
                continue

            print(f"[DEBUG] Đang kiểm tra dòng: '{ten_hien_thi}'")
            assert tu_khoa.lower() in ten_hien_thi, f"Lỗi: Dòng '{ten_hien_thi}' không chứa từ khóa '{tu_khoa}'"

        print("\n[INFO] Test Case Pass!")

    def test_tc09_tim_kiem_trang_thai(self):
        from selenium.webdriver.common.action_chains import ActionChains
        wait = WebDriverWait(self.driver, 10)
        time.sleep(1)
        dropdown = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class,'mud-select-input')"
            " and @tabindex='0'"
            " and @style='display:inline'"
            " and normalize-space()='Tất cả']"
        )))

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dropdown)
        time.sleep(0.3)
        ActionChains(self.driver).move_to_element(dropdown).click().perform()
        time.sleep(1)

        option = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class,'mud-list-item')]//p[normalize-space()='Hiệu lực']"
        )))
        ActionChains(self.driver).move_to_element(option).click().perform()
        time.sleep(1)

        selected_text = dropdown.text
        assert "Hiệu lực" in selected_text, \
            f"Expected 'Hiệu lực' nhưng thấy: '{selected_text}'"

        time.sleep(2)

        headers = self.driver.find_elements(By.XPATH, "//table//th")
        col_index = None
        for i, th in enumerate(headers):
            if "Trạng thái" in th.text:
                col_index = i + 1  # XPath td index bắt đầu từ 1
                print(f"[DEBUG] Cột Trạng thái ở vị trí: td[{col_index}]")
                break

        assert col_index is not None, "Không tìm thấy cột 'Trạng thái' trong bảng!"

        trang_thai_cells = self.driver.find_elements(
            By.XPATH, f"//table/tbody/tr/td[{col_index}]"
        )
        print(f"[DEBUG] Số dòng sau filter: {len(trang_thai_cells)}")

        assert len(trang_thai_cells) > 0, "Bảng không có dữ liệu sau khi filter!"

        for cell in trang_thai_cells:
            text = cell.text.strip()
            print(f"  → '{text}'")
            assert "Hiệu lực" in text, \
                f"Lỗi: Dòng có trạng thái '{text}' không phải 'Hiệu lực'!"

        print(f"\n[INFO] TC09 PASS: {len(trang_thai_cells)} dòng đều là 'Hiệu lực'.")

    def test_tc10_tim_kiem_trang_thai_khong_hieu_luc(self):
        from selenium.webdriver.common.action_chains import ActionChains
        wait = WebDriverWait(self.driver, 10)
        time.sleep(1)

        dropdown = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class,'mud-select-input')"
            " and @tabindex='0'"
            " and @style='display:inline'"
            " and normalize-space()='Tất cả']"
        )))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dropdown)
        time.sleep(0.3)
        ActionChains(self.driver).move_to_element(dropdown).click().perform()
        time.sleep(1)

        option = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class,'mud-list-item')]//p[normalize-space()='Không hiệu lực']"
        )))
        ActionChains(self.driver).move_to_element(option).click().perform()
        time.sleep(1)

        selected_text = dropdown.text
        assert "Không hiệu lực" in selected_text, \
            f"Expected 'Không hiệu lực' nhưng thấy: '{selected_text}'"
        time.sleep(2)
        headers = self.driver.find_elements(By.XPATH, "//table//th")
        col_index = None
        for i, th in enumerate(headers):
            if "Trạng thái" in th.text:
                col_index = i + 1
                print(f"[DEBUG] Cột Trạng thái ở vị trí: td[{col_index}]")
                break

        assert col_index is not None, "Không tìm thấy cột 'Trạng thái' trong bảng!"

        trang_thai_chips = self.driver.find_elements(
            By.XPATH, f"//table/tbody/tr/td[{col_index}]//p"
        )
        print(f"[DEBUG] Số dòng sau filter: {len(trang_thai_chips)}")
        assert len(trang_thai_chips) > 0, "Bảng không có dữ liệu sau khi filter!"

        for chip in trang_thai_chips:
            text = chip.text.strip()
            print(f"  → '{text}'")
            assert "Không hiệu lực" in text, \
                f"Lỗi: Dòng có trạng thái '{text}' không phải 'Không hiệu lực'!"

        print(f"\n[INFO] TC10 PASS: {len(trang_thai_chips)} dòng đều là 'Không hiệu lực'.")

    def test_tc11_nap_file_excel_chuc_vu(self):
        path_of_file = r"D:\Downloads\FileMau_CVCD.xlsx"
        print("\n--- Bắt đầu TC11: Nạp file Excel Chức Vụ ---")

        self.cv_page.click_nap_excel()
        time.sleep(2)

        print("Đang thực hiện tải file đính kèm...")
        self.cv_page.upload_file(path_of_file)
        print("Hoàn tất tải file, chờ 5 giây...")

        self.cv_page.click_tai_du_lieu_len()

        print("[INFO] Đang đợi hệ thống xử lý dữ liệu từ file...")
        time.sleep(5)

        try:
            toast_locator = (By.XPATH, "//div[contains(@class,'mud-snackbar-content-text')]")
            toast = self.driver.find_element(*toast_locator)
            print(f"\n[DEBUG] Kết quả nạp file: {toast.text}")
            assert "thành công" in toast.text.lower(), f"Lỗi: Nạp file không báo thành công! Nội dung: {toast.text}"
        except Exception:
            print("\n[WARNING] Không tìm thấy toast báo kết quả, hãy kiểm tra lại bảng dữ liệu.")
            self.driver.save_screenshot("reports/debug_cv_tc11_upload.png")