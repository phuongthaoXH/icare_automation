import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.d02_page import D02Page


@pytest.mark.giao_dien
class TestGiaoDienD02:
    def test_tc01_truy_cap_trang_d02(self, d02_page: D02Page):
        d02_page.wait_for_load()
        url = d02_page.get_url().lower()
        assert "thu-tuc" in url or "ke-khai" in url
        time.sleep(2)

    def test_tc02_bao_mat_duong_dan_url(self, d02_page: D02Page):
        url = d02_page.get_url().lower()
        for p in ["token=", "password=", "auth="]:
            assert p not in url, f"Cảnh báo: URL chứa thông tin nhạy cảm {p}"
        time.sleep(2)

    def test_tc03_chuyen_huong_khi_chua_dang_nhap(self, d02_page: D02Page):
        d02_page.driver.delete_all_cookies()
        d02_page.driver.refresh()
        WebDriverWait(d02_page.driver, 10).until(
            lambda d: "dang-nhap" in d.current_url.lower() or "login" in d.current_url.lower()
        )
        time.sleep(2)

    def test_tc04_hien_thi_cac_nut_chuc_nang(self, d02_page: D02Page):
        d02_page.wait_for_spinner_gone()
        buttons = [d02_page.BTN_LUU, d02_page.BTN_XOA_TAT_CA, d02_page.BTN_THEM_MOI_DONG]
        for btn in buttons:
            el = WebDriverWait(d02_page.driver, 7).until(EC.visibility_of_element_located(btn))
            assert el.is_displayed()
        time.sleep(2)

    def test_tc05_hien_thi_cac_cot_cua_bang(self, d02_page: D02Page):
        d02_page.wait_for_spinner_gone()
        expected_columns = [
            ("Họ và tên", "HoTen"),
            ("Phương án điều chỉnh", "PhuongAnId"),
            ("Ngày sinh", "NgaySinh"),
            ("Giới tính", "GioiTinh"),
            ("CMND/CCCD", "Cmnd"),
            ("Chức vụ", "ChucVu"),
            ("Số HĐLĐ/Quyết định", "SoHdlđ"),
            ("Ngày ký", "NgayKy"),
            ("Nơi làm việc", "NoiLamViec"),
            ("Tiền lương/ Hệ số", "TienLuong")
        ]
        print("\n--- Bắt đầu quét header bảng ---")

        for name, key in expected_columns:

            header_xpath = f"//th[normalize-space()='{name}']"
            cell_xpath = f"//div[@data-column-key='{key}']"

            try:
                header_el = WebDriverWait(d02_page.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, header_xpath))
                )
                if header_el.is_displayed():
                    print(f"PASS: Thấy cột '{name}'")
                else:
                    d02_page.driver.execute_script("arguments[0].scrollIntoView({inline: 'center'});", header_el)
                    print(f"PASS (Scrolled): Thấy cột '{name}'")

            except Exception as e:
                all_headers = d02_page.driver.find_elements(By.TAG_NAME, "th")
                actual_texts = [h.text.replace('\n', ' ').strip() for h in all_headers if h.text]
                print(f"LỖI: Không tìm thấy '{name}'.")
                print(f"Danh sách Header thực tế đang có: {actual_texts}")
                pytest.fail(f"Không tìm thấy cột {name}. Kiểm tra lại chính tả hoặc khoảng trắng!")

        print("--- Hoàn thành ---")

    def test_tc06_hien_thi_o_nhap_lieu(self, d02_page: D02Page):
        d02_page.wait_for_spinner_gone()
        el = WebDriverWait(d02_page.driver, 7).until(EC.visibility_of_element_located(d02_page.FLD_HO_TEN))
        assert el.tag_name == "input"
        time.sleep(2)

    def test_tc07_kiem_tra_thanh_tieu_de_co_dinh(self, d02_page: D02Page):
        header = d02_page.driver.find_element(By.TAG_NAME, "thead")
        assert "mud-table-head" in header.get_attribute("class")
        time.sleep(2)

    def test_tc08_hop_thoai_xac_nhan_xoa(self, d02_page: D02Page):
        d02_page.wait_for_spinner_gone()
        d02_page.click_element(d02_page.BTN_XOA_TAT_CA)
        time.sleep(2)

        dialog_xpath = "//div[contains(@class, 'mud-dialog')]//*[contains(text(), 'xóa') or contains(text(), 'Xác nhận')]"
        dialog = WebDriverWait(d02_page.driver, 5).until(EC.visibility_of_element_located((By.XPATH, dialog_xpath)))
        assert dialog.is_displayed()
        d02_page.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(2)

    def test_tc09_logic_di_chuyen_bang_phim_tab(self, d02_page: D02Page):
        d02_page.wait_for_spinner_gone()

        first_input = WebDriverWait(d02_page.driver, 10).until(
            EC.presence_of_element_located(d02_page.FLD_HO_TEN)
        )
        d02_page.driver.execute_script("arguments[0].click();", first_input)
        time.sleep(2)

        print("Bắt đầu nhấn Tab ...")
        for i in range(1, 35):
            current_active = d02_page.driver.switch_to.active_element
            current_active.send_keys(Keys.TAB)

            time.sleep(2)
            new_active = d02_page.driver.switch_to.active_element

        assert d02_page.driver.switch_to.active_element != first_input, "Focus không di chuyển sau khi Tab."

    def test_tc10_kiem_tra_giao_dien_co_gian_responsive(self, d02_page: D02Page):
        d02_page.driver.set_window_size(1024, 768)
        time.sleep(1)
        assert d02_page.driver.find_element(*d02_page.SEL_TABLE).is_displayed()
        d02_page.driver.maximize_window()
        time.sleep(2)