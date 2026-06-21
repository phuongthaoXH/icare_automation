import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time
from selenium.webdriver.common.keys import Keys # Thêm dòng này
from selenium.webdriver.support.wait import WebDriverWait
from pages.d02_page import D02Page
logger = logging.getLogger(__name__)

@pytest.mark.giao_dien
class TestD02DropdownLogic:

    def test_tc1_phuong_an_load_dung(self, d02_page: D02Page):
        d02_page.wait_for_spinner_gone()

        d02_page.select_mud_dropdown(d02_page.FLD_PHU_LUC, "Tăng lao động")
        time.sleep(1.5)

        d02_page.wait_and_click(d02_page.FLD_PHUONG_AN)
        time.sleep(1)

        assert "Tăng mới" in d02_page.driver.page_source or "TM" in d02_page.driver.page_source


    def test_tc2_loai_phuong_an_khac(self, d02_page: D02Page):
        d02_page.wait_for_spinner_gone()
        WebDriverWait(d02_page.driver, 10).until(EC.visibility_of_element_located(d02_page.FLD_PHU_LUC))

        d02_page.select_mud_dropdown(d02_page.FLD_PHU_LUC, "Khác")
        d02_page.select_mud_dropdown(d02_page.FLD_PHUONG_AN, "K")

        print("--- TC2: Đã chọn xong ---")


    def test_tc3_phuong_an_required_warning(self, d02_page: D02Page):
        d02_page.wait_for_spinner_gone()
        el = WebDriverWait(d02_page.driver, 10).until(
            EC.presence_of_element_located(d02_page.FLD_PHU_LUC)
        )
        d02_page.driver.execute_script("arguments[0].click();", el)

        el.send_keys(Keys.TAB)

        wait = WebDriverWait(d02_page.driver, 10)
        error_el = wait.until(EC.visibility_of_element_located(d02_page.LBL_ERROR_PHUONG_AN))
        actual_text = error_el.text.strip()

        print(f"DEBUG: Text thực tế tìm thấy: '{actual_text}'")

        assert "Trường không được trống" in actual_text

    def test_tc4_chon_ngan_hang(self, d02_page: D02Page):
        d02_page.wait_for_spinner_gone()
        d02_page.select_mud_dropdown(d02_page.FLD_TINH_NGAN_HANG, "Hà Nội")
        time.sleep(2)
        d02_page.wait_for_spinner_gone()
        d02_page.select_mud_dropdown(d02_page.FLD_TEN_NGAN_HANG, "01101001")

    def test_tc5_load_ngan_hang_theo_tinh(self, d02_page: D02Page):
        d02_page.wait_for_spinner_gone()
        d02_page.select_mud_dropdown(d02_page.FLD_TINH_NGAN_HANG, "04 - Tỉnh Cao Bằng")
        time.sleep(2)
        d02_page.wait_for_spinner_gone()
        d02_page.wait_and_click(d02_page.FLD_TEN_NGAN_HANG)
        time.sleep(1)

        options = d02_page.driver.find_elements(By.XPATH, "//div[contains(@class, 'mud-list-item')]")

        assert len(options) > 0, "LỖI: Danh sách Ngân hàng trống sau khi chọn tỉnh Cao Bằng!"
        print(f"TC5 Pass: Tìm thấy {len(options)} ngân hàng.")

    def test_tc6_chon_gioi_tinh(self, d02_page):
        d02_page.wait_for_spinner_gone()
        d02_page.select_mud_dropdown(d02_page.FLD_GIOI_TINH, "Nữ")

    def test_tc7_1_chon_loai_ngay_sinh_thang_nam(self, d02_page: D02Page):
        d02_page.wait_for_spinner_gone()

        el_loai_ns = d02_page.driver.find_element(*d02_page.FLD_LOAI_NGAY_SINH)
        d02_page.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            el_loai_ns
        )
        time.sleep(0.5)

        d02_page.wait_and_click(d02_page.FLD_LOAI_NGAY_SINH)
        time.sleep(0.8)

        xpath_thang_nam = "//div[contains(@class, 'mud-popover')]//div[contains(@class, 'mud-list-item')]//*[contains(text(), 'Tháng năm')]"

        try:
            wait = WebDriverWait(d02_page.driver, 5)
            item = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_thang_nam)))
            d02_page.driver.execute_script("arguments[0].scrollIntoView(true);", item)
            d02_page.driver.execute_script("arguments[0].click();", item)
            logger.info("Đã chọn 'Tháng năm' bằng cách click item.")
        except:
            logger.warning("Không click được item, thử dùng phím mũi tên...")
            el = d02_page.driver.find_element(*d02_page.FLD_LOAI_NGAY_SINH)

            el.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.3)

            el.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.3)

            el.send_keys(Keys.ENTER)

            d02_page.wait_for_spinner_gone()
            time.sleep(0.5)

        actual_text = d02_page.driver.find_element(*d02_page.FLD_LOAI_NGAY_SINH).text
        assert "Tháng năm" in actual_text
        logger.info(f"Đã chọn thành công '{actual_text}'")
        ngay_sinh_val = "11/1999"

        wait = WebDriverWait(d02_page.driver, 10)
        input_ngay_sinh = wait.until(EC.element_to_be_clickable(d02_page.FLD_NGAY_SINH))

        input_ngay_sinh.click()
        time.sleep(1)

        d02_page.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            input_ngay_sinh
        )
        time.sleep(0.5)

        input_ngay_sinh.send_keys(Keys.CONTROL + "a")
        input_ngay_sinh.send_keys(Keys.BACKSPACE)
        time.sleep(0.3)

        for char in ngay_sinh_val:
            input_ngay_sinh.send_keys(char)
            time.sleep(1)

        input_ngay_sinh.send_keys(Keys.TAB)

        logger.info(f"Đã nhập Ngày sinh: {ngay_sinh_val}")
        actual_val = input_ngay_sinh.get_attribute('value')
        assert ngay_sinh_val in actual_val
        logger.info(f"TC7.1 Hoàn tất: Giá trị hiển thị trên ô nhập là '{actual_val}'")

    def test_tc7_2_chon_loai_ngay_sinh_nam(self, d02_page: D02Page):
        d02_page.wait_for_spinner_gone()

        dropdown_el = d02_page.driver.find_element(*d02_page.FLD_LOAI_NGAY_SINH)
        d02_page.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            dropdown_el
        )
        time.sleep(0.5)

        d02_page.driver.execute_script("arguments[0].click();", dropdown_el)
        d02_page.driver.execute_script("arguments[0].focus();", dropdown_el)
        time.sleep(1.0)

        for _ in range(3):
            dropdown_el.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.2)

        dropdown_el.send_keys(Keys.ENTER)
        time.sleep(1.0)

        actual_text = d02_page.driver.execute_script("return arguments[0].textContent;", dropdown_el).strip()

        print(f"\nDebug - Text sau khi chọn: '{actual_text}'")
        assert "Năm" in actual_text, f"Lỗi: Giao diện vẫn hiển thị '{actual_text}'"

        ngay_sinh_val = "1999"

        wait = WebDriverWait(d02_page.driver, 10)
        input_ngay_sinh = wait.until(EC.element_to_be_clickable(d02_page.FLD_NGAY_SINH))

        input_ngay_sinh.click()
        time.sleep(0.3)

        input_ngay_sinh.send_keys(Keys.CONTROL + "a")
        input_ngay_sinh.send_keys(Keys.BACKSPACE)
        time.sleep(0.3)

        for char in ngay_sinh_val:
            input_ngay_sinh.send_keys(char)
            time.sleep(0.2)

        input_ngay_sinh.send_keys(Keys.ENTER)

        logger.info(f"Đã nhập Ngày sinh: {ngay_sinh_val}")

        actual_val = input_ngay_sinh.get_attribute('value')
        assert ngay_sinh_val in actual_val
        logger.info(f"TC7.2 Hoàn tất: Giá trị hiển thị trên ô nhập là '{actual_val}'")

    def test_tc7_3_chon_loai_ngay_sinh_day_du(self, d02_page: D02Page):
        d02_page.wait_for_spinner_gone()

        d02_page.wait_and_click(d02_page.FLD_LOAI_NGAY_SINH)
        time.sleep(1)

        xpath_day_du = "//div[contains(@class, 'mud-popover')]//div[contains(@class, 'mud-list-item')]//*[text()='Đầy đủ']"
        try:
            wait = WebDriverWait(d02_page.driver, 5)
            item = wait.until(EC.presence_of_element_located((By.XPATH, xpath_day_du)))
            d02_page.driver.execute_script("arguments[0].scrollIntoView(true);", item)
            d02_page.driver.execute_script("arguments[0].click();", item)
        except Exception as e:
            logger.warning(f"Thử dùng phím mũi tên: {e}")
            el_dropdown = d02_page.driver.find_element(*d02_page.FLD_LOAI_NGAY_SINH)
            el_dropdown.send_keys(Keys.ARROW_UP, Keys.ARROW_UP, Keys.ENTER)

        d02_page.wait_for_spinner_gone()
        time.sleep(0.5)

        ngay_sinh_val = "11111999"
        wait = WebDriverWait(d02_page.driver, 10)
        input_ngay_sinh = wait.until(EC.presence_of_element_located(d02_page.FLD_NGAY_SINH))

        d02_page.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                                       input_ngay_sinh)
        time.sleep(0.5)

        d02_page.driver.execute_script("arguments[0].click();", input_ngay_sinh)

        input_ngay_sinh.send_keys(Keys.CONTROL + "a")
        input_ngay_sinh.send_keys(Keys.BACKSPACE)
        time.sleep(0.3)

        for char in ngay_sinh_val:
            input_ngay_sinh.send_keys(char)
            time.sleep(1)

        input_ngay_sinh.send_keys(Keys.TAB)

        logger.info(f"Đã nhập từng số Ngày sinh: {ngay_sinh_val} và nhấn TAB")

        actual_val = input_ngay_sinh.get_attribute('value')
        logger.info(f"TC7.3 Hoàn tất: Giá trị hiển thị là '{actual_val}'")
        time.sleep(2)

    def test_tc8_ngay_ky(self, d02_page: D02Page):
        logger.info("Bắt đầu TC 8: Nhập Ngày ký hợp đồng (MudBlazor)")
        d02_page.wait_for_spinner_gone()

        ngay_ky_nhap = "05052026"
        ngay_ky_expected = "05/05/2026"
        wait = WebDriverWait(d02_page.driver, 15)

        try:
            input_xpath = "//div[@data-column-key='NgayKy']//input"
            input_element = wait.until(EC.presence_of_element_located((By.XPATH, input_xpath)))

            d02_page.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
                input_element
            )
            time.sleep(1)

            d02_page.driver.execute_script("arguments[0].click();", input_element)
            time.sleep(0.5)

            input_element.send_keys(Keys.CONTROL + "a")
            input_element.send_keys(Keys.BACKSPACE)
            time.sleep(0.3)

            for char in ngay_ky_nhap:
                input_element.send_keys(char)
                time.sleep(0.2)

            time.sleep(1)
            input_element.send_keys(Keys.TAB)
            logger.info(f"Đã nhập xong Ngày ký và nhấn TAB để ẩn dropdown")

            time.sleep(2)
            actual_val = input_element.get_attribute('value')
            assert ngay_ky_expected in actual_val
            logger.info(f"TC 8 thành công: Giá trị hiển thị là {actual_val}")

        except Exception as e:
            logger.error(f"Lỗi thực thi TC 8: {str(e)}")
            raise e

    def fill_thang_nam(self, d02_page: D02Page, tu_thang: str, den_thang: str):
        wait = WebDriverWait(d02_page.driver, 10)
        xpath_tu = "//div[@data-column-key='TuThang']//input"
        xpath_den = "//div[@data-column-key='DenThang']//input"

        for xpath, value in [(xpath_tu, tu_thang), (xpath_den, den_thang)]:
            clean_value = value.replace("/", "")

            el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

            d02_page.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", el)
            time.sleep(0.5)
            d02_page.driver.execute_script("arguments[0].click();", el)

            el.send_keys(Keys.CONTROL + "a")
            el.send_keys(Keys.BACKSPACE)
            time.sleep(0.5)

            for char in clean_value:
                el.send_keys(char)
                time.sleep(0.3)

            time.sleep(1)
            el.send_keys(Keys.TAB)
            time.sleep(0.8)

            actual_val = el.get_attribute('value')
            if value not in actual_val:
                logger.warning(f"Nhập chưa đủ! Kỳ vọng {value} nhưng mới có {actual_val}. Đang thử lại...")
                el.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
                for char in clean_value:
                    el.send_keys(char)
                    time.sleep(0.3)
                el.send_keys(Keys.TAB)

    def test_tc9_tu_thang_nho_hon_den_thang(self, d02_page: D02Page):
        logger.info("Bắt đầu TC 9: Từ tháng < Đến tháng")
        d02_page.wait_for_spinner_gone()

        self.fill_thang_nam(d02_page, "01/2026", "05/2026")

        val_tu = d02_page.driver.find_element(By.XPATH, "//div[@data-column-key='TuThang']//input").get_attribute(
            'value')
        val_den = d02_page.driver.find_element(By.XPATH, "//div[@data-column-key='DenThang']//input").get_attribute(
            'value')

        assert "01/2026" in val_tu, f"Lỗi: Ô Từ tháng hiển thị sai ({val_tu})"
        assert "05/2026" in val_den, f"Lỗi: Ô Đến tháng hiển thị sai ({val_den})"

        error_elements = d02_page.driver.find_elements(By.XPATH, "//div[contains(text(), 'Dữ liệu không hợp lệ.')]")
        assert len(error_elements) == 0, "Lỗi: Hiện thông báo sai lệch khi dữ liệu hợp lệ"

        logger.info(f"TC 9 PASSED chuẩn: Từ {val_tu} đến {val_den}")
        time.sleep(2)

    def test_tc10_tu_thang_lon_hon_den_thang(self, d02_page: D02Page):
        logger.info("Bắt đầu TC 10: Từ tháng > Đến tháng")
        d02_page.wait_for_spinner_gone()

        self.fill_thang_nam(d02_page, "03/2026", "01/2026")

        val_tu = d02_page.driver.find_element(By.XPATH, "//div[@data-column-key='TuThang']//input").get_attribute(
            'value')
        val_den = d02_page.driver.find_element(By.XPATH, "//div[@data-column-key='DenThang']//input").get_attribute(
            'value')

        assert "03/2026" in val_tu, f"Lỗi: Ô Từ tháng hiển thị sai ({val_tu})"
        assert "01/2026" in val_den, f"Lỗi: Ô Đến tháng hiển thị sai ({val_den})"

        logger.info(f"Đã nhập xong: Từ {val_tu} - Đến {val_den}. Đang kiểm tra thông báo lỗi...")

        time.sleep(1.5)
        error_xpath = "//div[contains(text(), 'Dữ liệu không hợp lệ.')]"
        error_elements = d02_page.driver.find_elements(By.XPATH, error_xpath)

        assert len(error_elements) > 0, "Lỗi: Hệ thống KHÔNG hiển thị cảnh báo khi Từ tháng > Đến tháng"

        logger.info("TC 10 PASSED: Thông báo 'Dữ liệu không hợp lệ.' đã hiển thị chính xác.")
        time.sleep(2)

    def test_tc11_tu_thang_bang_den_thang(self, d02_page: D02Page):
        logger.info("Bắt đầu TC 11: Từ tháng = Đến tháng")
        d02_page.wait_for_spinner_gone()

        self.fill_thang_nam(d02_page, "03/2026", "03/2026")

        val_tu = d02_page.driver.find_element(By.XPATH, "//div[@data-column-key='TuThang']//input").get_attribute(
            'value')
        val_den = d02_page.driver.find_element(By.XPATH, "//div[@data-column-key='DenThang']//input").get_attribute(
            'value')

        assert "03/2026" in val_tu, f"Lỗi: Ô Từ tháng chưa nhập đủ hoặc sai định dạng ({val_tu})"
        assert "03/2026" in val_den, f"Lỗi: Ô Đến tháng chưa nhập đủ hoặc sai định dạng ({val_den})"

        logger.info(f"Dữ liệu thực tế: Từ {val_tu} - Đến {val_den}. Đang kiểm tra lỗi...")

        time.sleep(1)
        error_elements = d02_page.driver.find_elements(By.XPATH, "//div[contains(text(), 'Dữ liệu không hợp lệ.')]")

        assert len(error_elements) == 0, "Lỗi: Hệ thống báo 'Dữ liệu không hợp lệ' khi Từ tháng bằng Đến tháng"

        logger.info("TC 11 PASSED: Dữ liệu bằng nhau được chấp nhận và không có lỗi hiển thị.")
        time.sleep(2)

    def fill_numeric_cell(self, d02_page: D02Page, column_key: str, value: str):
        wait = WebDriverWait(d02_page.driver, 10)
        xpath = f"//div[@data-column-key='{column_key}']//input"

        el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

        d02_page.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'instant', block: 'center', inline: 'center'});", el
        )
        time.sleep(0.5)

        d02_page.driver.execute_script("arguments[0].click();", el)
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(Keys.BACKSPACE)
        time.sleep(0.3)

        for char in str(value):
            el.send_keys(char)
            time.sleep(0.2)

        time.sleep(0.5)
        el.send_keys(Keys.TAB)

        time.sleep(0.5)
        logger.info(f"Đã nhập xong giá trị {value} vào cột {column_key}")

    def test_tc12_nhap_tien_luong_hop_le(self, d02_page: D02Page):
        logger.info("Bắt đầu TC 12: Nhập tiền lương hợp lệ (Max 15 ký tự)")
        d02_page.wait_for_spinner_gone()

        val_max = "999999999999999"

        try:
            self.fill_numeric_cell(d02_page, "TienLuong", val_max)
            time.sleep(2)
            self.fill_numeric_cell(d02_page, "PhuCapLuong", "5000000")
            time.sleep(2)
            self.fill_numeric_cell(d02_page, "PhuCapBoSung", "1000000")
            time.sleep(2)

            logger.info("TC 12 Pass: Đã nhập thành công các giá trị lương dài.")
            time.sleep(1)
        except Exception as e:
            logger.error(f"TC 12 Fail: {str(e)}")
            raise e

    def test_tc13_nhap_luong_am_reset_ve_0(self, d02_page: D02Page):
        logger.info("Bắt đầu TC 13: Nhập lương âm để kiểm tra reset")
        d02_page.wait_for_spinner_gone()

        try:
            self.fill_numeric_cell(d02_page, "TienLuong", "-5000000")
            time.sleep(2)
            self.fill_numeric_cell(d02_page, "PhuCapLuong", "-5000000")
            time.sleep(2)
            self.fill_numeric_cell(d02_page, "PhuCapBoSung", "-1000000")
            time.sleep(2)

            el = d02_page.driver.find_element(By.XPATH, "//div[@data-column-key='TienLuong']//input")
            actual_val = el.get_attribute("value").replace(".", "").replace(",", "")

            assert actual_val == "0", f"Lỗi: Nhập số âm nhưng giá trị là {actual_val}, không phải 0"
            logger.info("TC 13 Pass: Hệ thống đã tự động reset lương âm về 0.")
            time.sleep(1)
        except Exception as e:
            logger.error(f"TC 13 Fail: {str(e)}")
            raise e

    def test_tc14_nhap_luong_khac_so_tu_dong_xoa(self, d02_page: D02Page):
        logger.info("Bắt đầu TC 14: Nhập chữ vào ô lương")
        d02_page.wait_for_spinner_gone()

        try:
            self.fill_numeric_cell(d02_page, "TienLuong", "abcxyz")
            time.sleep(2)
            self.fill_numeric_cell(d02_page, "PhuCapLuong", "a")
            time.sleep(2)
            self.fill_numeric_cell(d02_page, "PhuCapBoSung", "b")
            time.sleep(2)

            el = d02_page.driver.find_element(By.XPATH, "//div[@data-column-key='TienLuong']//input")
            actual_val = el.get_attribute("value").strip()

            assert actual_val == "" or actual_val == "0", f"Lỗi: Nhập chữ nhưng ô lương vẫn hiển thị: {actual_val}"
            logger.info("TC 14 Pass: Hệ thống đã tự động xóa ký tự không phải số.")
            time.sleep(1)
        except Exception as e:
            logger.error(f"TC 14 Fail: {str(e)}")
            raise e

    def check_dong_theo_he_so(self, d02_page: D02Page):
        wait = WebDriverWait(d02_page.driver, 10)
        checkbox_container_xpath = "//div[@data-column-key='HeSoMucLuong']//input[@type='checkbox']"
        checkbox = wait.until(EC.presence_of_element_located((By.XPATH, checkbox_container_xpath)))

        if not checkbox.is_selected():
            d02_page.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                                           checkbox)
            time.sleep(0.5)
            d02_page.driver.execute_script("arguments[0].click();", checkbox)
            logger.info("Đã tích chọn 'Đóng theo hệ số'")
            time.sleep(0.5)

    def fill_he_so_cell(self, d02_page: D02Page, column_key: str, value: str):
        driver = d02_page.driver
        wait = WebDriverWait(driver, 10)
        cell_xpath = f"//div[@data-column-key='{column_key}']"
        input_xpath = f"{cell_xpath}//input"

        try:
            cell_div = wait.until(EC.presence_of_element_located((By.XPATH, cell_xpath)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", cell_div)
            time.sleep(0.8)

            input_el = wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
            driver.execute_script("arguments[0].click();", input_el)
            time.sleep(0.5)

            input_el.send_keys(Keys.CONTROL + "a")
            time.sleep(0.3)
            input_el.send_keys(Keys.BACKSPACE)
            time.sleep(0.5)

            for char in str(value):
                input_el.send_keys(char)
                time.sleep(0.2)

            time.sleep(1)
            input_el.send_keys(Keys.TAB)
            time.sleep(0.5)

            logger.info(f"Đã nhập xong: {value} vào cột: {column_key}")

        except Exception as e:
            logger.error(f"Lỗi tại cột {column_key}: {str(e)}")
            raise e

    def test_tc15_nhap_he_so_hop_le(self, d02_page: D02Page):
        logger.info("Bắt đầu TC 15: Nhập hệ số hợp lệ")
        try:
            self.check_dong_theo_he_so(d02_page)

            self.fill_he_so_cell(d02_page, "TienLuong", "13")
            time.sleep(2)
            self.fill_he_so_cell(d02_page, "PhuCapChucVu", "1.3")
            time.sleep(2)
            self.fill_he_so_cell(d02_page, "PhuCapThamNienVuotKhung", "10")
            time.sleep(2)
            self.fill_he_so_cell(d02_page, "PhuCapThamNienNghe", "5")
            time.sleep(2)

            logger.info("TC 15 Pass: Đã nhập đầy đủ các loại hệ số và phụ cấp.")
        except Exception as e:
            logger.error(f"TC 15 Fail: {str(e)}")
            raise e

    def test_tc16_nhap_he_so_am_reset_0(self, d02_page: D02Page):
        logger.info("Bắt đầu TC 16: Kiểm tra reset giá trị âm về 0")
        d02_page.wait_for_spinner_gone()

        test_data = [
            {"name": "Hệ số lương", "key": "TienLuong", "value": "-5"},
            {"name": "Phụ cấp CV", "key": "PhuCapChucVu", "value": "-1.5"},
            {"name": "Phụ cấp TNVK", "key": "PhuCapThamNienVuotKhung", "value": "-10"},
            {"name": "Phụ cấp TNN", "key": "PhuCapThamNienNghe", "value": "-20"}
        ]

        try:
            self.check_dong_theo_he_so(d02_page)

            for item in test_data:
                column_key = item["key"]
                input_value = item["value"]
                column_name = item["name"]

                self.fill_he_so_cell(d02_page, column_key, input_value)

                input_xpath = f"//div[@data-column-key='{column_key}']//input"
                el = d02_page.driver.find_element(By.XPATH, input_xpath)
                el.send_keys(Keys.TAB)

                time.sleep(1)

                raw_val = el.get_attribute("value").replace(".", "").replace(",", "").strip()

                actual_num = int(raw_val) if raw_val.isdigit() else -1

                assert actual_num == 0, f"Lỗi: Cột {column_name} không reset về 0 (Giá trị thực tế: {raw_val})"
                logger.info(f"Xác nhận: Cột {column_name} đã reset về 0.")

            logger.info("TC 16 Pass: Đã kiểm tra xong các trường hệ số.")

        except Exception as e:
            logger.error(f"TC 16 Fail: {str(e)}")
            raise e

    def test_tc17_nhap_he_so_khac_so_tu_dong_xoa(self, d02_page: D02Page):
        logger.info("Bắt đầu TC 17: Nhập chữ vào hệ số để kiểm tra tự động xóa")
        d02_page.wait_for_spinner_gone()

        test_data = [
            {"name": "Hệ số lương", "key": "TienLuong", "value": "abc"},
            {"name": "Phụ cấp CV", "key": "PhuCapChucVu", "value": "xyz"},
            {"name": "Phụ cấp TNVK", "key": "PhuCapThamNienVuotKhung", "value": "khongso"},
            {"name": "Phụ cấp TNN", "key": "PhuCapThamNienNghe", "value": "!!!"}
        ]

        try:
            self.check_dong_theo_he_so(d02_page)

            for item in test_data:
                column_key = item["key"]
                input_value = item["value"]
                column_name = item["name"]

                self.fill_he_so_cell(d02_page, column_key, input_value)

                input_xpath = f"//div[@data-column-key='{column_key}']//input"
                el = d02_page.driver.find_element(By.XPATH, input_xpath)
                el.send_keys(Keys.TAB)

                time.sleep(0.8)

                actual_val = el.get_attribute("value").strip()

                actual_num = 0
                if actual_val != "":
                    clean_val = actual_val.replace(".", "").replace(",", "")
                    actual_num = int(clean_val) if clean_val.isdigit() else -1
                else:
                    actual_num = 0

                assert actual_num == 0, f"Lỗi: Cột {column_name} không xóa ký tự chữ (Giá trị thực tế: {actual_val})"
                logger.info(f"Xác nhận: Cột {column_name} đã tự động xóa ký tự '{input_value}'.")

            logger.info("TC 17 Pass: Hệ thống đã chặn và xóa các ký tự không phải số thành công.")

        except Exception as e:
            logger.error(f"TC 17 Fail: {str(e)}")
            raise e